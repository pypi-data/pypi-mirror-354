# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 Kevin De Bruycker and Stijn D'hollander
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
# from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from numba import njit
import dash
from dash import dcc, html, Input, Output, State
from spycontrol import import_spycontrol_data
# import plotly.io as pio
# pio.renderers.default = 'browser'










def GUI():
    plot_size = (5, 4.5)
    max_exponentials = 5
    sg.theme('Dark Grey 7')
    icon_base64 = b''


    InputParameters = [
        [
            sg.Text("Experiment:"),
        ],
        [
            sg.Radio('Stress relaxation', 'ExperimentType', pad=(5, 0), disabled=True, key="-StressRelaxation-"),
        ],
        [
            sg.Radio('Frequency sweep', 'ExperimentType', pad=(5, 0), disabled=True, key="-FrequencySweep-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text("Read temperature from:"),
        ],
        [
            sg.Radio('Additional column in table', 'get_T_from', pad=(5, 0), default=True, disabled=True, key="-T_from_datacolumns_names_last-"),
        ],
        [
            sg.Radio('Last number in curve header', 'get_T_from', pad=(5, 0), disabled=True, key="-T_from_curve_header_last_number-"),
        ],
        [
            sg.Text("Temperature unit:"),
            sg.DropDown(['°C', 'K'], default_value='°C', disabled=True, size=(4, 1), key="-T_unit-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text('Discard first'),
            sg.Spin([i for i in range(0, 101)], initial_value=0, pad=(0, 3), size=(3,1), disabled=True, key='-datapoints_discarded-'),
            sg.Text('data points'),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Button('Open file', disabled=True, key='-OpenFile-')
        ],
    ]

    ParameterColumn1 = [
        [
            sg.Frame("Input parameters:", InputParameters, key="-InputParameters-")
        ],
    ]

    RelaxationTimeSelection = [
        [
            sg.Radio('Intersect with 1/e', 'tau_mode', pad=(5, 0), enable_events=True, default=True, disabled=True, key="-TauModeIntersect-"),
        ],
        [
            sg.Radio('Advanced', 'tau_mode', pad=(5, 0), enable_events=True, disabled=True, key="-TauModeAdvanced-"),
        ],

    ]

    TemperatureSelection = [
        [
            sg.Listbox(values=[], disabled=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                       size=(13, 3), no_scrollbar=True, key="-Temperatures-"),
        ],
        [
            sg.Button('Update', disabled=True, key='-UpdateTemperatures-')
        ],
    ]

    ParameterColumn2 = [
        [
            sg.Frame("Relaxation time:", RelaxationTimeSelection, key="-RelaxationTimeSelection-")
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Frame("Temperatures:", TemperatureSelection, key="-TemperatureSelection-")
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Checkbox("Normalise G(t)", pad=(5, 0), enable_events=True, default=True, disabled=True,
                        key="-normalise_relax_mod-"),
        ],
    ]

    InputColumn = [
        [
            sg.Text("File:"),
            sg.InputText(size=(41, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(("CSV/Text file", ["*.csv", "*.txt"]), ("All files", "*.*"), )),
        ],
        [
            sg.Column(ParameterColumn1, vertical_alignment='top'),
            sg.Column(ParameterColumn2, vertical_alignment='top'),
        ],
    ]

    DataPlotColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-DataPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenDataPlot-'),
            sg.Save('Save CSV', disabled=True, key='-QuickSaveDataPlotCSV-'),
            sg.Save('Save XLSX', disabled=True, key='-QuickSaveDataPlotXLSX-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveDataPlotAs-"),
            sg.FileSaveAs('Save raw plot data as...', disabled=True, file_types=(("Excel file", "*.xlsx"), ("CSV file", "*.csv"), ),
                          key='-SaveDataPlot-', ),
        ],
    ]

    ArrheniusColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-ArrheniusPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenArrheniusPlot-'),
            sg.Save('Save CSV', disabled=True, key='-QuickSaveArrheniusPlotCSV-'),
            sg.Save('Save XLSX', disabled=True, key='-QuickSaveArrheniusPlotXLSX-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveArrheniusPlotAs-"),
            sg.FileSaveAs('Save raw plot data as...', disabled=True, file_types=(("Excel file", "*.xlsx"), ("CSV file", "*.csv"), ),
                          key='-SaveArrheniusPlot-', ),
        ],
    ]

    OverviewTab = [
        [
            sg.Column(DataPlotColumn),
            sg.VSeperator(),
            sg.Column(ArrheniusColumn),
        ],
    ]

    CurveByCurveParams = [
        [
            sg.Text("Select temperature:"),
        ],
        [
            sg.Listbox(values=[], enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(13, 3),
                       no_scrollbar=True, key="-CurveByCurve_temperature-"),
        ],
        [
            sg.Checkbox("Analyse curve", pad=(5, 0), enable_events=True, default=True, disabled=True, key="-CurveByCurve_visible-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Radio('Intersect with 1/e', 'TauModel', pad=(5, 0), disabled=True, enable_events=True,
                     key="-TauModel_intersect-",
                     tooltip='Determines the intersect with 1/e and assumes a simple Maxwellian behaviour\n'
                             '(i.e. single exponential decay of stress vs. time)'),
        ],
        [
            sg.Text("Fit model:"),
        ],
        [
            sg.Radio('Single Maxwell', 'TauModel', pad=(5, 0), disabled=True, enable_events=True,
                     key="-TauModel_single-",
                     tooltip=''),
        ],
        [
            sg.Radio('Stretched Maxwell', 'TauModel', pad=(5, 0), disabled=True, enable_events=True,
                     key="-TauModel_stretched_single-",
                     tooltip=''),
        ],
        [
            sg.Radio('Generalised (liquid)', 'TauModel', pad=(5, 0), disabled=True, default=True, enable_events=True,
                     key="-TauModel_generalised_liquid-",
                     tooltip='Fits a number of exponentials (and thus Maxwell elements) to the relaxation curve'),
        ],
        [
            sg.Radio('Stretched gen. (liquid)', 'TauModel', pad=(5, 0), disabled=True, enable_events=True,
                     key="-TauModel_stretched_generalised_liquid-",
                     tooltip=''),
        ],
        [
            sg.Text('  ', pad=(5, 0)),
            sg.Text('Elements: '),
            sg.Spin([i for i in range(1, max_exponentials + 1)], initial_value=1, pad=((0, 10), 3), size=(3, 1), enable_events=True, disabled=True,
                    key='-TauModel_exponentials-'),
        ],
    ]

    Weights = [
        [
            sg.Text("Weights:"),
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(19, max_exponentials), disabled=True,
                       no_scrollbar=True, key="-AdvancedResults_weights-"),
        ],
    ]

    StretchFactors = [
        [
            sg.Text("Stretch factors:"),
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(19, max_exponentials), disabled=True,
                       no_scrollbar=True, key="-AdvancedResults_stretches-"),
        ],
    ]

    RelaxationTimes = [
        [
            sg.Text("Relaxation times:"),
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(19, max_exponentials), disabled=True,
                       no_scrollbar=True, key="-AdvancedResults_times-"),
        ],
    ]

    AdvancedResults = [
        [
            sg.Column(RelaxationTimes, vertical_alignment='top')
        ],
        [
            sg.Column(Weights, vertical_alignment='top'),
            sg.Column(StretchFactors, vertical_alignment='top')
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text('Use relaxation time', tooltip='To assemble the Arrhenius plot. Applies to exponential fits only.'),
            sg.Spin([i for i in range(1, max_exponentials + 1)], initial_value=1, pad=(0, 3), size=(3, 1),
                    enable_events=True, key='-time_idx-',
                    tooltip='To assemble the Arrhenius plot. Applies to exponential fits only.'),
            sg.Text('(high to low)', tooltip='To assemble the Arrhenius plot. Applies to exponential fits only.'),
        ],
        [
            sg.Button('Apply', key='-AdvancedResults_apply-'),
        ],
    ]

    AdvancedParameterColumn = [
        [
            sg.Frame("Curve-by-curve:", CurveByCurveParams, key="-CurveByCurve-"),
            sg.Frame("Results:", AdvancedResults, key="-AdvancedResults-", vertical_alignment='top'),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Save('Save Maxwell data', key='-QuickSaveMaxwellData-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveMaxwellDataAs-"),
            sg.FileSaveAs('Save Maxwell data as...',
                          file_types=(("Excel file", "*.xlsx"),),
                          key='-SaveMaxwellData-', ),
        ],
        # [
        #     sg.Text("", pad=(5, 0)),
        # ],
    ]

    CurveFitColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-CurveFitPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenCurveFitPlot-'),
            # sg.Save('Save CSV', disabled=True, key='-QuickSaveMaxwellPlotCSV-'),
            # sg.Save('Save XLSX', disabled=True, key='-QuickSaveMaxwellPlotXLSX-'),
            # sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveMaxwellPlotAs-"),
            # sg.FileSaveAs('Save raw plot data as...', disabled=True,
            #               file_types=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"),),
            #               key='-SaveMaxwellPlot-', ),
        ],
    ]

    AdvancedTab = [
        [
            sg.Column(AdvancedParameterColumn, size=(plot_size[0] * 102, plot_size[1] * 100)),
            sg.VSeperator(),
            sg.Column(CurveFitColumn),
        ],
    ]

    Tabs = [
        [
            sg.Tab('Overview', OverviewTab, key="-OverviewTab-"),
            sg.Tab('Advanced', AdvancedTab, key="-AdvancedTab-", visible=False),
        ],
    ]

    layout = [
        [
            sg.Column(InputColumn),
            sg.TabGroup(Tabs)
            # sg.VSeperator(),
            # sg.Column(DataPlotColumn),
            # sg.VSeperator(),
            # sg.Column(ArrheniusColumn),
        ],
    ]

    window = sg.Window("Anton Paar Rheology v" + aprheology.__version__, layout)
    window.Finalize()

    def draw_plot(canvas, plot):
        for child in canvas.winfo_children():
            child.destroy()
        if plot:
            figure_canvas_agg = FigureCanvasTkAgg(plot, canvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    def update_overview_plots(experiment):
        draw_plot(window['-DataPlot-'].TKCanvas, experiment.plot(plot_size=plot_size, return_plot=True))
        draw_plot(window['-ArrheniusPlot-'].TKCanvas, experiment.analyse_arrhenius(plot_size=plot_size, show_plot=False, return_plot=True))

    def update_curve_fit(experiment, values):
        if experiment.get_evaluate_flag(values['-CurveByCurve_temperature-'][0]):
            if values['-TauModel_intersect-']:
                draw_plot(window['-CurveFitPlot-'].TKCanvas,
                          experiment.plot_SM(temperature=values['-CurveByCurve_temperature-'][0],
                                             plot_size=plot_size,
                                             return_plot=True))
            else:
                if values['-TauModel_single-']:
                    model = 'single'
                elif values['-TauModel_stretched_single-']:
                    model = 'stretched single'
                elif values['-TauModel_generalised_liquid-']:
                    model = 'generalised liquid'
                elif values['-TauModel_stretched_generalised_liquid-']:
                    model = 'stretched generalised liquid'
                try:
                    draw_plot(window['-CurveFitPlot-'].TKCanvas,
                              experiment.fit_curve(exponentials=values['-TauModel_exponentials-'],
                                                   model=model,
                                                   curve_temp=values['-CurveByCurve_temperature-'][0],
                                                   plot_size=plot_size,
                                                   return_plot=True))
                except:
                    values['-TauModel_intersect-'] = True
                    draw_plot(window['-CurveFitPlot-'].TKCanvas,
                              experiment.plot_SM(temperature=values['-CurveByCurve_temperature-'][0],
                                                 plot_size=plot_size,
                                                 return_plot=True))
                    values['-TauModel_single-'] = False
                    values['-TauModel_stretched_single-'] = False
                    values['-TauModel_generalised_liquid-'] = False
                    values['-TauModel_stretched_generalised_liquid-'] = False
                    sg.popup_error('Something went wrong fitting curves, please use different settings.')

        else:
            draw_plot(window['-CurveFitPlot-'].TKCanvas, None)

    def get_updated_advancedresults(experiment, values):
        if experiment.get_evaluate_flag(values['-CurveByCurve_temperature-'][0]):
            if values['-TauModel_intersect-']:
                experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_fit'] = False
                return [], [], [str(round(experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_intersect'], 3))]
            else:
                experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_fit'] = True
                if values['-TauModel_single-']:
                    weights = []
                    stretches = []
                    times = list(u'{:.3f} \u00B1 {:.3f}'.format(round(time, 3), round(time_err, 3)) for
                                 time, time_err in
                                 experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, -2:])
                elif values['-TauModel_stretched_single-']:
                    weights = []
                    stretches = list(u'{:.3f} \u00B1 {:.3f}'.format(round(stretch, 3), round(stretch_err, 3)) for
                                     stretch, stretch_err in
                                     experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, 0:2])
                    times = list(u'{:.3f} \u00B1 {:.3f}'.format(round(time, 3), round(time_err, 3)) for
                                 time, time_err in
                                 experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, -2:])
                elif values['-TauModel_generalised_liquid-']:
                    weights = list(u'{:.3f} \u00B1 {:.3f}'.format(round(weight, 3), round(weight_err, 3)) for
                                   weight, weight_err in
                                   experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, 0:2])
                    stretches = []
                    times = list(u'{:.3f} \u00B1 {:.3f}'.format(round(time, 3), round(time_err, 3)) for
                                 time, time_err in
                                 experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, -2:])
                elif values['-TauModel_stretched_generalised_liquid-']:
                    weights = list(u'{:.3f} \u00B1 {:.3f}'.format(round(weight, 3), round(weight_err, 3)) for
                                   weight, weight_err in
                                   experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, 0:2])
                    stretches = list(u'{:.3f} \u00B1 {:.3f}'.format(round(stretch, 3), round(stretch_err, 3)) for
                                     stretch, stretch_err in
                                     experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, 2:4])
                    times = list(u'{:.3f} \u00B1 {:.3f}'.format(round(time, 3), round(time_err, 3)) for
                                 time, time_err in
                                 experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'][:, -2:])
                return weights, stretches, times
        return [], [], []

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FILE-":
            if not values["-FILE-"]:
                continue
            try:
                window["-T_unit-"].update(aprheology.RelaxationExperiment(values["-FILE-"], None).T_unit)
            except:
                pass
            window["-StressRelaxation-"].update(disabled=False)
            window["-FrequencySweep-"].update(disabled=False)
            window["-T_from_datacolumns_names_last-"].update(disabled=False)
            window["-T_from_curve_header_last_number-"].update(disabled=False)
            window["-T_unit-"].update(disabled=False)
            # window["-tau_mode_interpolate-"].update(disabled=False)
            # window["-tau_mode_closest-"].update(disabled=False)
            # window["-datapoints_discarded-"].update(disabled=False)
            # Gives an error that a wrong state is passed... Do it manually without update:
            window["-datapoints_discarded-"].TKSpinBox['state'] = 'normal'
            window["-OpenFile-"].update(disabled=False)
        if event == "-OpenFile-":
            if values['-T_from_datacolumns_names_last-']:
                get_T_from = 'datacolumns_names_last'
            elif values['-T_from_curve_header_last_number-']:
                get_T_from = 'curve_header_last_number'
            else:
                sg.popup_error('Something went wrong')
                continue
            # if values['-tau_mode_interpolate-']:
            #     tau_mode = 'interpolate_highest'
            # elif values['-tau_mode_closest-']:
            #     tau_mode = 'closest_highest'
            # else:
            #     sg.popup_error('Something went wrong')
            #     continue
            datapoints_discarded = int(values['-datapoints_discarded-']) if values['-datapoints_discarded-'] != 0 else None
            if values['-StressRelaxation-']:
                try:
                    experiment = aprheology.StressRelaxation(filename=values["-FILE-"],
                                                             get_T_from=get_T_from,
                                                             T_unit=values["-T_unit-"],
                                                             datapoints_discarded=datapoints_discarded,
                                                             normalise_relax_mod=values["-normalise_relax_mod-"])
                    window["-TauModeIntersect-"].update(disabled=False, value=True)
                    window["-TauModeAdvanced-"].update(disabled=False)
                    window["-normalise_relax_mod-"].update(disabled=False)
                except:
                    sg.popup_error('Something went wrong, check the input file.')
                    continue
            elif values['-FrequencySweep-']:
                try:
                    experiment = aprheology.FrequencySweep(filename=values["-FILE-"],
                                                           get_T_from=get_T_from,
                                                           T_unit=values["-T_unit-"],
                                                           datapoints_discarded=datapoints_discarded)
                    window["-TauModeIntersect-"].update(disabled=True)
                    window["-TauModeAdvanced-"].update(disabled=True)
                    window["-normalise_relax_mod-"].update(disabled=True)
                except:
                    sg.popup_error('Something went wrong, check the input file.')
                    continue
            else:
                sg.popup_error('No experiment type selected.')
                continue
            update_overview_plots(experiment)
            window["-Temperatures-"].update(disabled=False)
            temperatures = [curve['T'] for curve in experiment.curves]
            window["-Temperatures-"].update(values=temperatures)
            window["-Temperatures-"].SetValue(temperatures)
            window["-Temperatures-"].set_size(size=(None, len(temperatures)))
            window["-UpdateTemperatures-"].update(disabled=False)
            window['-OpenDataPlot-'].update(disabled=False)
            window['-OpenArrheniusPlot-'].update(disabled=False)
            window['-QuickSaveDataPlotCSV-'].update(disabled=False)
            window['-QuickSaveDataPlotXLSX-'].update(disabled=False)
            window['-SaveDataPlot-'].update(disabled=False)
            window['-QuickSaveArrheniusPlotCSV-'].update(disabled=False)
            window['-QuickSaveArrheniusPlotXLSX-'].update(disabled=False)
            window['-SaveArrheniusPlot-'].update(disabled=False)
            window['-AdvancedTab-'].update(visible=False)
            window["-Temperatures-"].update(disabled=False)
            window["-UpdateTemperatures-"].update(disabled=False)
            window["-CurveByCurve_temperature-"].update(values=temperatures)
            window["-CurveByCurve_temperature-"].set_size(size=(None, len(temperatures)))
        if event == "-normalise_relax_mod-":
            try:
                experiment.normalised_relax_mod = values["-normalise_relax_mod-"]
                update_overview_plots(experiment)
            except:
                pass
        if event == '-TauModeIntersect-':
            for curve in experiment.curves:
                curve['tau'] = curve['tau_intersect']
                curve['tau_mode_fit'] = False
            update_overview_plots(experiment)
            window['-AdvancedTab-'].update(visible=False)
            window["-Temperatures-"].update(disabled=False)
            window["-UpdateTemperatures-"].update(disabled=False)
        if event == '-TauModeAdvanced-':
            window['-AdvancedTab-'].update(visible=True)
            window["-Temperatures-"].update(disabled=True)
            window["-UpdateTemperatures-"].update(disabled=True)
        if event == '-UpdateTemperatures-':
            experiment.set_evaluated_T(T_list=values["-Temperatures-"])
            update_overview_plots(experiment)
        if event == '-OpenDataPlot-':
            experiment.plot(return_plot=False)
        if event == '-OpenArrheniusPlot-':
            experiment.analyse_arrhenius(show_plot=True, return_plot=False)
        if event == '-QuickSaveDataPlotCSV-':
            try:
                experiment.export_plot_data(excel=False)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-QuickSaveArrheniusPlotCSV-':
            try:
                experiment.export_arrhenius_data(excel=False)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-QuickSaveDataPlotXLSX-':
            try:
                experiment.export_plot_data(excel=True)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-QuickSaveArrheniusPlotXLSX-':
            try:
                experiment.export_arrhenius_data(excel=True)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-SaveDataPlotAs-':
            extension = re.sub('\A.*\.([^.]*)\Z', '\\1', values['-SaveDataPlotAs-'])
            try:
                experiment.export_plot_data(filename=values['-SaveDataPlotAs-'], excel=(extension == 'xlsx'))
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-SaveArrheniusPlotAs-':
            extension = re.sub('\A.*\.([^.]*)\Z', '\\1', values['-SaveArrheniusPlotAs-'])
            try:
                experiment.export_arrhenius_data(filename=values['-SaveArrheniusPlotAs-'], excel=(extension == 'xlsx'))
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-CurveByCurve_temperature-':
            evaluate_flag = experiment.get_evaluate_flag(values['-CurveByCurve_temperature-'][0])
            window["-CurveByCurve_visible-"].update(disabled=False,
                                                    value=evaluate_flag)
            window["-TauModel_intersect-"].update(disabled=not evaluate_flag)
            window["-TauModel_single-"].update(disabled=not evaluate_flag)
            window["-TauModel_stretched_single-"].update(disabled=not evaluate_flag)
            window["-TauModel_generalised_liquid-"].update(disabled=not evaluate_flag)
            window["-TauModel_stretched_generalised_liquid-"].update(disabled=not evaluate_flag)
            try:
                number_exponentials = len(experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit'])
                if experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_fit']:
                    model = experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_fit_model']
                    if model == 'single':
                        window["-TauModel_single-"].update(value=True)
                        values["-TauModel_intersect-"] = False
                        values["-TauModel_single-"] = True
                        values["-TauModel_stretched_single-"] = False
                        values["-TauModel_generalised_liquid-"] = False
                        values["-TauModel_stretched_generalised_liquid-"] = False
                    elif model == 'stretched single':
                        window["-TauModel_stretched_single-"].update(value=True)
                        values["-TauModel_intersect-"] = False
                        values["-TauModel_single-"] = False
                        values["-TauModel_stretched_single-"] = True
                        values["-TauModel_generalised_liquid-"] = False
                        values["-TauModel_stretched_generalised_liquid-"] = False
                    elif model == 'generalised liquid':
                        window["-TauModel_generalised_liquid-"].update(value=True)
                        values["-TauModel_intersect-"] = False
                        values["-TauModel_single-"] = False
                        values["-TauModel_stretched_single-"] = False
                        values["-TauModel_generalised_liquid-"] = True
                        values["-TauModel_stretched_generalised_liquid-"] = False
                    elif model == 'stretched generalised liquid':
                        window["-TauModel_stretched_generalised_liquid-"].update(value=True)
                        values["-TauModel_intersect-"] = False
                        values["-TauModel_single-"] = False
                        values["-TauModel_stretched_single-"] = False
                        values["-TauModel_generalised_liquid-"] = False
                        values["-TauModel_stretched_generalised_liquid-"] = True
                else:
                    window["-TauModel_intersect-"].update(value=True)
                    values["-TauModel_intersect-"] = True
                    values["-TauModel_single-"] = False
                    values["-TauModel_stretched_single-"] = False
                    values["-TauModel_generalised_liquid-"] = False
                    values["-TauModel_stretched_generalised_liquid-"] = False
                window["-TauModel_exponentials-"].update(disabled=not evaluate_flag or (
                        not values['-TauModel_generalised_liquid-'] and not values['-TauModel_stretched_generalised_liquid-']),
                                                         value=number_exponentials)
                values["-TauModel_exponentials-"] = number_exponentials
            except:
                # window["-TauModel_generalised_liquid-"].update(value=True)
                # values["-TauModel_intersect-"] = False
                # values["-TauModel_single-"] = False
                # values["-TauModel_stretched_single-"] = False
                # values["-TauModel_generalised_liquid-"] = True
                # values["-TauModel_stretched_generalised_liquid-"] = False
                window["-TauModel_exponentials-"].update(disabled=not evaluate_flag or (not values['-TauModel_generalised_liquid-'] and not values['-TauModel_stretched_generalised_liquid-']))
                # experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_fit'] = True
            window["-AdvancedResults_weights-"].update(disabled=not evaluate_flag)
            window["-AdvancedResults_times-"].update(disabled=not evaluate_flag)
            window["-AdvancedResults_stretches-"].update(disabled=not evaluate_flag)
            window["-OpenCurveFitPlot-"].update(disabled=not evaluate_flag)
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == '-CurveByCurve_visible-':
            window["-TauModel_exponentials-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-TauModel_single-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-TauModel_stretched_single-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-TauModel_generalised_liquid-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-TauModel_stretched_generalised_liquid-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-TauModel_intersect-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-AdvancedResults_weights-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-AdvancedResults_times-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-AdvancedResults_stretches-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-OpenCurveFitPlot-"].update(disabled=not values['-CurveByCurve_visible-'])
            experiment.set_evaluate_flag(values['-CurveByCurve_temperature-'][0], values['-CurveByCurve_visible-'])
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == "-TauModel_intersect-":
            window["-TauModel_exponentials-"].update(disabled=True)
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == "-TauModel_single-":
            window["-TauModel_exponentials-"].update(disabled=True)
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == "-TauModel_stretched_single-":
            window["-TauModel_exponentials-"].update(disabled=True)
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == "-TauModel_generalised_liquid-":
            window["-TauModel_exponentials-"].update(disabled=False)
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == "-TauModel_stretched_generalised_liquid-":
            window["-TauModel_exponentials-"].update(disabled=False)
            update_curve_fit(experiment, values)
            weights, stretches, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
            window["-AdvancedResults_stretches-"].update(values=stretches)
        if event == "-TauModel_exponentials-":
            try:
                update_curve_fit(experiment, values)
                weights, stretches, times = get_updated_advancedresults(experiment, values)
                window["-AdvancedResults_weights-"].update(values=weights)
                window["-AdvancedResults_times-"].update(values=times)
                window["-AdvancedResults_stretches-"].update(values=stretches)
            except:
                sg.popup_error('Select a temperature first')
        # if event == "-time_idx-":
        #     get_updated_relaxation_times(experiment, values)
        if event == "-AdvancedResults_apply-":
            experiment.set_arrhenius_times(values['-time_idx-'] - 1)
            update_overview_plots(experiment)
        if event == "-OpenCurveFitPlot-":
            if values['-TauModel_intersect-']:
                experiment.plot_SM(temperature=values['-CurveByCurve_temperature-'][0],
                                   return_plot=False)
            else:
                experiment.fit_curve(exponentials=values['-TauModel_exponentials-'],
                                     curve_temp=values['-CurveByCurve_temperature-'][0],
                                     return_plot=False)
        if event == "-QuickSaveMaxwellData-":
            try:
                experiment.export_maxwell_data()
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == "-SaveMaxwellDataAs-":
            try:
                experiment.export_maxwell_data(filename=values['-SaveMaxwellDataAs-'])
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")




    window.close()