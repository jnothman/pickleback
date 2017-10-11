import pickle
import subprocess


def test_with_script(tmpdir):
    tmpdir.join('plot.py').write('import sys\n'
                                 'import matplotlib.pyplot as plt\n'
                                 'import matplotlib\n'
                                 'matplotlib.use("Agg")\n'
                                 'plt.scatter([5, 6, 7], [8, 9, 10])\n'
                                 'plt.title("Hello world")\n'
                                 'plt.savefig(sys.argv[1])\n'
                                 )
    script_path = str(tmpdir.join('plot.py'))
    subprocess.check_call(['python', script_path,
                           str(tmpdir.join('plot.raw'))])
    subprocess.check_call(['python', '-m', 'pickleback', script_path,
                           str(tmpdir.join('plot.pkl'))])
    fig = pickle.load(open(str(tmpdir.join('plot.pkl')), 'rb'))
    # FIXME: fig.canvas comes back None. I've not yet understood why/how
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    fig.canvas = FigureCanvas(fig)
    fig.savefig(str(tmpdir.join('plot-via-pkl.raw')))
    expected_bytes = tmpdir.join('plot.raw').read(mode='rb')
    actual_bytes = tmpdir.join('plot-via-pkl.raw').read(mode='rb')
    assert expected_bytes == actual_bytes
