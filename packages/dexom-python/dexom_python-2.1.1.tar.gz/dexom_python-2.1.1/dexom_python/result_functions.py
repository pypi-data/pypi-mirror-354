import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from warnings import warn
from cobra import Solution
from sklearn.decomposition import PCA
from dexom_python.default_parameter_values import DEFAULT_VALUES


def write_solution(model, solution, threshold, filename='imat_sol.csv'):
    """
    Writes an optimize solution as a txt file. The solution is written in a column format

    Parameters
    ----------
    solution: cobra.Solution
    threshold: float
    filename: str
    """
    tol = model.solver.configuration.tolerances.feasibility
    solution_binary = (np.abs(solution.fluxes) >= threshold-tol).values.astype(int)
    with open(filename, 'w+') as file:
        file.write('reaction,fluxes,binary\n')
        for i, v in enumerate(solution.fluxes):
            file.write(solution.fluxes.index[i]+','+str(v)+','+str(solution_binary[i])+'\n')
        file.write('objective value: %f\n' % solution.objective_value)
        file.write('solver status: %s' % solution.status)
    return solution, solution_binary


def read_solution(filename, model=None, reaction_weights=None, solution_index=0, eps=DEFAULT_VALUES['epsilon'],
                  thr=DEFAULT_VALUES['threshold']):
    """
    Reads a solution from a .csv file. If the provided file is a file containing fluxes
    (as output by enumeration methods), the solution number solution_index will be read

    Parameters
    ----------
    filename: str
        name of the file containing the solution
    model: cobra.Model
        optional unless the filename points to a solution file without reaction IDs
    reaction_weights: dict
        optional unless the filename points to a flux file, in which case it is needed for calculating objective values
    solution_index: int
        defines which solution will be read from the binary solution file
    eps: float
    thr: float

    Returns
    -------
    solution: cobra.Solution
    sol_bin: numpy.array
    """
    fluxflag = True
    with open(filename, 'r') as f:
        reader = f.read().split('\n')
        if reader[0] == 'reaction,fluxes,binary':
            fluxflag = False
            if reader[-1] == '':
                reader.pop(-1)
            objective_value = float(reader[-2].split()[-1])
            status = reader[-1].split()[-1]
    if fluxflag:
        df = pd.read_csv(filename, index_col=0, sep=';|,|\t', engine='python')
        fluxes = df.iloc[solution_index % (len(df)-1)]
        if model is not None:
            fluxes.index = [rxn.id for rxn in model.reactions]
        else:
            print('A model is necessary for setting the reaction IDs in a flux solution. '
                  'Disregard this message if the columns of the flux solution are already reaction IDs')
        sol_bin = np.array(fluxes.values)
        if reaction_weights is None or model is None:
            objective_value = -1.
        else:
            objective_value = calc_objval_from_flux(fluxes, model=model, rw=reaction_weights, eps=eps, thr=thr)
        status = 'flux'
    else:
        df = pd.read_csv(filename, index_col=0, skipfooter=2, sep=';|,|\t', engine='python')
        fluxes = df['fluxes']
        sol_bin = df['binary'].to_list()
    solution = Solution(objective_value, status, fluxes)
    return solution, sol_bin


def calc_objval_from_flux(fluxsol, model, rw, eps=DEFAULT_VALUES['epsilon'], thr=DEFAULT_VALUES['threshold']):
    """
    Calculates the objective value of a solution based on the flux values

    Parameters
    ----------
    fluxsol: pandas.Series
        a flux solution in which the index contains the model reaction IDs
    model: cobra.model
    rw: dict
    eps: float
    thr: float

    Returns
    -------
    objval: float
    """
    objval = 0
    for r, w in rw.items():
        if w > 0 and np.abs(fluxsol[r]) >= eps-model.tolerance:
            objval += w
        elif w < 0 and  np.abs(fluxsol[r]) < thr + model.tolerance:
            objval -= w
    return objval


def compile_solutions(solutions, out_path='compiled_solutions', solution_pattern='*.csv', model=None, threshold=None):
    """
    Compiles individual solution files into one binary solution DataFrame

    Parameters
    ----------
    solutions: list or str
        If list, must contain either solution files in .csv format, or Solution objects, or binary solution arrays. -
        If str, must be a folder in which the solution files math the sollution_pattern parameter
    out_path: str
        path to which the combined solutions will be saved
    solution_pattern: str
        If reading solutions from a folder, this is the pattern which will be used to recognize solution files
    model: cobrapy Model
        required  if the solutions parameter is a list of Solution objects
    threshold: float
        required if the solutions parameter is a list of Solution objects

    Returns
    -------
    sol_frame: pandas DataFrame containg binary solutions
    """
    if model is not None:
        tol = model.solver.configuration.tolerances.feasibility
    else:
        tol = None
    if isinstance(solutions, str):
        sol_paths = [str(x) for x in Path(solutions).glob(solution_pattern)]
    else:
        sol_paths = solutions
    sols = []
    for s in sol_paths:
        binsol = None
        if isinstance(s, str):
            fullsol, binsol = read_solution(s, model=model)
        elif isinstance(s, Solution):
            try:
                binsol = (np.abs(s.fluxes) >= threshold - tol).values.astype(int)
            except TypeError:
                warn('If you pass a list of Solution objects, you must also provide the model and threshold parameters.'
                     'The current model parameter is %s and the current threshold parameter is %s' % (model, threshold))
        elif isinstance(s, list) or isinstance(s, np.ndarray):
            binsol = np.array(s)
        else:
            warn('Unrecognized type %s for solution %s' % (type(s), s))
        if binsol is not None:
            sols.append(binsol)
    sol_frame = pd.DataFrame(sols).drop_duplicates(ignore_index=True)
    sol_frame.to_csv(out_path+'.csv')
    return sol_frame


def plot_pca(solution_path, rxn_enum_solutions=None, save=True, save_name=''):
    """
    Plots a 2-dimensional PCA of enumeration solutions

    Parameters
    ----------
    solution_path: str
        csv file of enumeration solutions
    rxn_enum_solutions: str
        csv file of enumeration solutions. If specified, will plot these solutions in a different color
    save: bool
        if True, the pca-plot will be saved
    save_name: str
        name of the file to save

    Returns
    -------
    pca: sklearn.decomposition.PCA
    """
    X = pd.read_csv(solution_path, index_col=0, sep=';|,|\t', engine='python')

    if rxn_enum_solutions is not None:
        X2 = pd.read_csv(rxn_enum_solutions, index_col=0, sep=';|,|\t', engine='python')
        X_t = pd.concat([X, X2])
    else:
        X_t = X

    pca = PCA(n_components=2)
    pca.fit(X_t)

    comp = pca.transform(X)
    x = [c[0] for c in comp]
    y = [c[1] for c in comp]

    if rxn_enum_solutions is not None:
        comp2 = pca.transform(X2)
        x2 = [c[0] for c in comp2]
        y2 = [c[1] for c in comp2]

    plt.clf()
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=14)
    plt.xlabel(f'Principal Component 1 (explained variance: {np.around(pca.explained_variance_ratio_[0], 1)}%)', fontsize=20)
    plt.ylabel(f'Principal Component 2 (explained variance: {np.around(pca.explained_variance_ratio_[1], 1)}%)', fontsize=20)
    plt.title('PCA of enumeration solutions', fontsize=20)
    if rxn_enum_solutions is not None:
        plt.scatter(x2, y2, color='g', label='rxn-enum solutions')
        plt.scatter(x, y, color='b', label='div-enum solutions')
    else:
        plt.scatter(x, y, color='b', label='enumeration solutions')
    plt.scatter(x[0], y[0], color='r', label='iMAT solution')
    plt.legend(fontsize='large')
    if save:
        fig.savefig(save_name+'pca.png')
    return pca


def _main():
    """
    This function is called when you run this script from the commandline.
    It plots a 2-dimensional PCA of enumeration solutions and saves as png
    Use --help to see commandline parameters
    """
    description = 'Plots a 2-dimensional PCA of enumeration solutions and saves as png'
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--solutions', default=argparse.SUPPRESS, help='csv file of enumeration solutions')
    parser.add_argument('-r', '--rxn_solutions', default=None,
                        help='(optional) csv file containing reaction-enumeration solutions')
    parser.add_argument('-o', '--out_path', default='', help='name of the file which will be saved')
    args = parser.parse_args()

    pca = plot_pca(args.solutions, rxn_enum_solutions=args.rxn_solutions, save_name=args.out_path)
    return True


if __name__ == '__main__':
    _main()
