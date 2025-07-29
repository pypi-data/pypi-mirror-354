# skip linting for this file

import itertools
import os
import typing as t
import warnings

import ase.io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import zntrack
from ase.optimize import BFGS
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram as pmg_PhaseDiagram
from pymatgen.analysis.pourbaix_diagram import PourbaixDiagram as pmg_PourbaixDiagram
from pymatgen.analysis.pourbaix_diagram import (
    PourbaixEntry,
    PourbaixPlotter,
)
from pymatgen.core import Element
from pymatgen.core.ion import Ion
from pymatgen.entries.compatibility import (
    MaterialsProject2020Compatibility,
    MaterialsProjectAqueousCompatibility,
)
from pymatgen.entries.computed_entries import (
    ComputedEntry,
    GibbsComputedStructureEntry,
)

from mlipx.abc import ComparisonResults, NodeWithCalculator


def create_pourbaix_plot(
    self,
    limits=None,
    title="Pourbaix Diagram",
    label_domains=True,
    label_fontsize=12,
    show_water_lines=True,
    show_neutral_axes=True,
) -> go.Figure:
    PREFAC = 0.0591  # Prefactor for water stability lines

    # Set default limits if not provided
    if limits is None:
        limits = [[-2, 16], [-3, 3]]
    xlim, ylim = limits

    # Initialize Plotly figure
    fig = go.Figure()

    # Add water stability lines
    if show_water_lines:
        h_line_x = np.linspace(xlim[0], xlim[1], 100)
        h_line_y = -h_line_x * PREFAC
        o_line_y = -h_line_x * PREFAC + 1.23
        fig.add_trace(
            go.Scatter(
                x=h_line_x,
                y=h_line_y,
                mode="lines",
                line={"color": "red", "dash": "dash"},
                name="H2O Reduction",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=h_line_x,
                y=o_line_y,
                mode="lines",
                line={"color": "red", "dash": "dash"},
                name="H2O Oxidation",
            )
        )

    # Add neutral axes
    if show_neutral_axes:
        fig.add_trace(
            go.Scatter(
                x=[7, 7],
                y=ylim,
                mode="lines",
                line={"color": "grey", "dash": "dot"},
                name="Neutral Axis",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xlim,
                y=[0, 0],
                mode="lines",
                line={"color": "grey", "dash": "dot"},
                name="V=0 Line",
            )
        )

    # Add stable domain polygons
    for entry, vertices in self._pbx._stable_domain_vertices.items():
        # Close the polygon by repeating the first vertex
        vertices = np.vstack([vertices, vertices[0]])
        x, y = vertices[:, 0], vertices[:, 1]
        center = np.mean(vertices, axis=0)

        # Add the domain polygon
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line={"color": "grey"},
                name=f"Domain {entry.name}",
            )
        )

        # Optionally add labels to domains
        if label_domains:
            fig.add_trace(
                go.Scatter(
                    x=[center[0]],
                    y=[center[1]],
                    mode="text",
                    text=[entry.to_pretty_string()],
                    textfont={"size": label_fontsize, "color": "blue"},
                    name="Domain Label",
                )
            )

    # Update layout for the figure
    fig.update_layout(
        title={
            "text": title,
            "font": {"size": 20, "family": "Arial", "weight": "bold"},
        },
        xaxis={"title": "pH", "range": xlim},
        yaxis={"title": "E (V)", "range": ylim},
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    return fig


class PourbaixDiagram(zntrack.Node):
    """Compute the Pourbaix diagram for a given set of structures.

    Parameters
    ----------
    data : list[ase.Atoms]
        List of structures to evaluate.
    model : NodeWithCalculator
        Node providing the calculator object for the energy calculations.
    pH : float
        pH where the Pourbaix stability is evaluated ,
    V : float
        Electrode potential where the Pourbaix stability is evaluated.
    use_gibbs : bool, default=False
        Set to 300 (for 300 Kelvin) to use a machine learning model to
        estimate solid free energy from DFT energy (see
        GibbsComputedStructureEntry). This can slightly improve the accuracy
        of the Pourbaix diagram in some cases. Default: None. Note that
        temperatures other than 300K are not permitted here, because
        MaterialsProjectAqueousCompatibility corrections, used in Pourbaix
        diagram construction, are calculated based on 300 K data.
    data_ids : list[int], default=None
        Index of the structure to evaluate.
    geo_opt: bool, default=False
        Whether to perform geometry optimization before calculating the
        Pourbaix decomposition energy of each structure.
    fmax: float, default=0.05
        The maximum force stopping rule for geometry optimizations.

    Attributes
    ----------
    results : pd.DataFrame
        DataFrame with the data_id, potential energy and Pourbaix
        decomposition energy.
    plots : dict[str, go.Figure]
        Dictionary with the phase diagram (and Pourbaix decomposition
        energy plot).

    """

    model: NodeWithCalculator = zntrack.deps()
    data: list[ase.Atoms] = zntrack.deps()
    pH: float = zntrack.params()
    V: float = zntrack.params()
    use_gibbs: bool = zntrack.params(False)
    data_ids: list[int] = zntrack.params(None)
    geo_opt: bool = zntrack.params(False)
    fmax: float = zntrack.params(0.05)
    frames_path: str = zntrack.outs_path(zntrack.nwd / "frames.xyz")
    results: pd.DataFrame = zntrack.plots(
        x="data_id", y="pourbaix_decomposition_energy"
    )
    pourbaix_diagram: t.Any = zntrack.outs()

    def run(self):  # noqa: C901
        if self.data_ids is None:
            atoms_list = self.data
        else:
            atoms_list = [self.data[i] for i in self.data_id]
        if self.model is not None:
            calc = self.model.get_calculator()

        try:
            api_key = os.environ["MP_API_KEY"]
        except KeyError:
            raise KeyError("Please set the environment variable `MP_API_KEY`.")

        mpr = MPRester(api_key)
        U_metal_set = {"Co", "Cr", "Fe", "Mn", "Mo", "Ni", "V", "W"}
        U_settings = {
            "Co": 3.32,
            "Cr": 3.7,
            "Fe": 5.3,
            "Mn": 3.9,
            "Mo": 4.38,
            "Ni": 6.2,
            "V": 3.25,
            "W": 6.2,
        }
        solid_compat = MaterialsProject2020Compatibility()
        chemsys = set(
            itertools.chain.from_iterable(atoms.symbols for atoms in atoms_list)
        )
        # capitalize and sort the elements
        chemsys = sorted(e.capitalize() for e in chemsys)
        if isinstance(chemsys, str):
            chemsys = chemsys.split("-")
        # download the ion reference data from MPContribs
        ion_data = mpr.get_ion_reference_data_for_chemsys(chemsys)
        # build the PhaseDiagram for get_ion_entries
        ion_ref_comps = [
            Ion.from_formula(d["data"]["RefSolid"]).composition for d in ion_data
        ]
        ion_ref_elts = set(
            itertools.chain.from_iterable(i.elements for i in ion_ref_comps)
        )
        # TODO - would be great if the commented line below would work
        # However for some reason you cannot process GibbsComputedStructureEntry with
        # MaterialsProjectAqueousCompatibility
        ion_ref_entries = mpr.get_entries_in_chemsys(
            list([str(e) for e in ion_ref_elts] + ["O", "H"]), use_gibbs=self.use_gibbs
        )

        epots, new_ion_ref_entries, metal_comp_dicts, metallic_ids = [], [], [], []
        for i, atoms in enumerate(atoms_list):
            metals = [s for s in set(atoms.symbols) if s not in ["O", "H"]]
            hubbards = {}
            if set(metals) & U_metal_set:
                run_type = "GGA+U"
                is_hubbard = True
                for m in metals:
                    hubbards[m] = U_settings.get(m, 0)
            else:
                run_type = "GGA"
                is_hubbard = False

            if self.model is not None:
                atoms.calc = calc
            if self.geo_opt:
                dyn = BFGS(atoms)
                dyn.run(fmax=self.fmax)
            epot = atoms.get_potential_energy()
            ase.io.write(self.frames_path, atoms, append=True)
            epots.append(epot)
            amt_dict = {
                m: len([a for a in atoms if a.symbol == m]) for m in set(atoms.symbols)
            }
            n_metals = len([a for a in atoms if a.symbol not in ["O", "H"]])
            if n_metals > 0:
                metal_comp_dict = {m: amt_dict[m] / n_metals for m in metals}
                metallic_ids.append(i)
                metal_comp_dicts.append(metal_comp_dict)
            entry = ComputedEntry(
                composition=amt_dict,
                energy=epot,
                parameters={
                    "run_type": run_type,
                    "software": "N/A",
                    "oxide_type": "oxide",
                    "is_hubbard": is_hubbard,
                    "hubbards": hubbards,
                },
            )
            new_ion_ref_entries.append(entry)
        ion_ref_entries = new_ion_ref_entries + ion_ref_entries
        # suppress the warning about supplying the required energies;
        #  they will be calculated from the
        # entries we get from MPRester
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="You did not provide the required O2 and H2O energies.",
            )
            compat = MaterialsProjectAqueousCompatibility(solid_compat=solid_compat)
        # suppress the warning about missing oxidation states
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Failed to guess oxidation states.*"
            )
            ion_ref_entries = compat.process_entries(ion_ref_entries)  # type: ignore

        # TODO - if the commented line above would work, this conditional block
        # could be removed
        if self.use_gibbs:
            # replace the entries with GibbsComputedStructureEntry
            ion_ref_entries = GibbsComputedStructureEntry.from_entries(
                ion_ref_entries, temp=self.use_gibbs
            )
        ion_ref_pd = pmg_PhaseDiagram(ion_ref_entries)
        ion_entries = mpr.get_ion_entries(ion_ref_pd, ion_ref_data=ion_data)
        pbx_entries = [PourbaixEntry(e, f"ion-{n}") for n, e in enumerate(ion_entries)]

        # Construct the solid pourbaix entries from filtered ion_ref entries
        extra_elts = (
            set(ion_ref_elts)
            - {Element(s) for s in chemsys}
            - {Element("H"), Element("O")}
        )
        new_pbx_entries = []
        for entry in ion_ref_entries:
            entry_elts = set(entry.composition.elements)
            # Ensure no OH chemsys or extraneous elements from ion references
            if not (
                entry_elts <= {Element("H"), Element("O")}
                or extra_elts.intersection(entry_elts)
            ):
                # Create new computed entry
                eform = ion_ref_pd.get_form_energy(entry)  # type: ignore
                new_entry = ComputedEntry(
                    entry.composition, eform, entry_id=entry.entry_id
                )
                pbx_entry = PourbaixEntry(new_entry)
                new_pbx_entries.append(pbx_entry)

        pbx_entries = new_pbx_entries + pbx_entries
        row_dicts = []
        epbx_min = 10000.0
        for i, atoms in enumerate(atoms_list):
            if self.data_ids is None:
                data_id = i
            else:
                data_id = self.data_id[i]
            if i in metallic_ids:
                idx = metallic_ids.index(i)
                entry = pbx_entries[idx]
                pbx_dia = pmg_PourbaixDiagram(
                    pbx_entries, comp_dict=metal_comp_dicts[idx]
                )
                epbx = pbx_dia.get_decomposition_energy(entry, pH=self.pH, V=self.V)
                if epbx < epbx_min:
                    self.pourbaix_diagram = pbx_dia
                    epbx_min = epbx
            else:
                epbx = 0.0
            row_dicts.append(
                {
                    "data_id": data_id,
                    "potential_energy": epots[i],
                    "pourbaix_decomposition_energy": epbx,
                },
            )
        self.results = pd.DataFrame(row_dicts)

    @property
    def figures(self) -> dict[str, go.Figure]:
        # Create the Pourbaix diagram plot using Matplotlib
        plotter = PourbaixPlotter(self.pourbaix_diagram)

        return {
            "pourbaix-diagram": create_pourbaix_plot(plotter),
            "pourbaix-decomposition-energy-plot": px.line(
                self.results, x="data_id", y="pourbaix_decomposition_energy"
            ),
        }

    @staticmethod
    def compare(*nodes: "PourbaixDiagram") -> ComparisonResults:
        figures = {}

        for node in nodes:
            # Extract a unique identifier for the node
            node_identifier = node.name.replace(f"_{node.__class__.__name__}", "")

            # Update and store the figures directly
            for key, fig in node.figures.items():
                fig.update_layout(title=node_identifier)
                figures[f"{node_identifier}-{key}"] = fig

        return {
            "frames": nodes[0].frames,
            "figures": figures,
        }

    @property
    def frames(self) -> list[ase.Atoms]:
        with self.state.fs.open(self.frames_path, "r") as f:
            return list(ase.io.iread(f, format="extxyz"))
