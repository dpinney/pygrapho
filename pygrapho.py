''' pygrapho, visualize gigantic graphs the interactive, ElGrapho way.'''
import random
import json
import tempfile
import os
import webbrowser

_MYDIR = os.path.abspath(os.path.dirname(__file__))

_EL_GRAPHO_LIB = open(f'{_MYDIR}/ElGrapho.2.4.0.min.js').read()

_HTML_SLUG = open(f'{_MYDIR}/ElGrapho.html').read()

LAYOUT_TYPES = ['ForceDirected', 'Tree', 'RadialTree', 'Hairball', 'Chord', 'Cluster', 'None']

MODEL_SCHEMA_EXAMPLE = {
	'nodes':[
		{'x':0, 'y':0.6, 'group':0, 'label':0},
		{'x':-0.4, 'y': 0, 'group': 1, 'label': 1},
	],
	'edges':[
		{'from:':0, 'to':1},
		{'from':0, 'to':2},
	]
}

OPTIONS = {
	'width':'number that defines the width of the El Grapho viewport in pixels. The default is 500.',
	'height':'number defines the height of the El Grapho viewport in pixels. The default is 500.',
	'nodeSize':'number between 0 and 1 which defines the node size. The default is 1.',
	'nodeOutline':'boolean that enables or disables node outlines. The default is true.',
	'edgeSize':'number between 0 and 1 which defines the edge size. Edge sizes are relative to the connecting node size. The default is 0.25.',
	'darkMode':'boolean that enables or disables dark mode. The default is false.',
	'glowBlend':'number between 0 and 1 that defines the glow blending of nodes and edges. A value of 0 has no glow blending, and a value of 1 has full glow blending. Glow blending can be used as a visual treatment to emphasize node clustering or edge bundling. It is most effective when used in conjunction with dark mode. The default is 0.',
	'fillContainer':'boolean that enables or disables auto filling the container. When true, El Grapho will automatically detect anytime its container has changed shape, and will auto resize itself. The default is false.',
	'tooltips':'boolean that enables or disables tooltips. The default is true.',
	'arrows':'boolean that enables or disables edge arrows. For non directed or bi-directional graphs, you should keep arrows as false. The default is false.',
	'animations':'boolean that defines animation strategy. When animations is true, zoom and pan transitions will be animated. Otherwise the transitions will be immediate. Although animations utilize requestAnimationFrame for dynamic frame rates, in some situations you may prefer to set animations to false to improve transition performance for very high cardinality graphs with millions of nodes and edges. The default is true.',
	'debug':'boolean that can be used to enable debug mode. Debug mode will show the node and edge count in the bottom right corner of the visualization. The default is false.',
}

def _render(model, options, layout, file_out=False):
	''' Helper function to build the html for an elgrapho display. '''
	clean_model = str(model)
	clean_options = json.dumps(options).replace('{','').replace('}','')
	if layout == 'None':
		clean_layout = 'model'
	elif layout in LAYOUT_TYPES:
		clean_layout = f'ElGrapho.layouts.{layout}(model)'
	else:
		print(f'Invalid layout. Must be one of {LAYOUT_TYPES}')
		return None
	if file_out:
		styling = 'style="width:100%; height:100vh"'
	else:
		styling = '' # small container for jupyter
	contents = _HTML_SLUG.replace('ELGRAPHO_LIB', _EL_GRAPHO_LIB).replace('MODEL_INSERT_HERE',clean_model).replace('GRAPHO_OPTIONS_HERE',clean_options).replace('MODEL_TYPE_HERE',clean_layout).replace('STYLING_INSERT_HERE', styling)
	return contents

def render_jup(model, options, layout):
	''' Render in jupyter a [model] with [options] and a given [layout].
	For valid formats, see pygrapho.MODEL_SCHEMA and pygrapho.OPTIONS'''
	from IPython.core.display import display, HTML
	contents = _render(model, options, layout)
	return display(HTML(contents))

def render_file(model, options, layout, path=None, open_file=False):
	''' Render to file with a [model] with [options] and a given [layout].
	You can choose the [path] you want the file written to, and [open_file=True] if you want to see the results immediately in a browser.
	For valid formats, see pygrapho.MODEL_SCHEMA and pygrapho.OPTIONS'''
	contents = _render(model, options, layout, file_out=True)
	if path is None:
		fd, tmp_path = tempfile.mkstemp()
		path = tmp_path + '.html' # for opening later
		print(fd, tmp_path)
		with os.fdopen(fd, 'w') as out_file:
			out_file.write(contents)
		os.rename(tmp_path, path)
	else:
		with open(path, 'w') as out_file:
			out_file.write(contents)
	if open_file:
		webbrowser.open_new(f'file://{path}')

def _chord_model_example():
	NUM_NODES = 10000;
	NODE_RAN = range(0, NUM_NODES)
	NUM_NODES_FIRST_GROUP = round(NUM_NODES * 0.25);
	model = {
		'nodes': [{'group':(0 if n < NUM_NODES_FIRST_GROUP else 1)} for n in NODE_RAN],
		'edges': [{'from': random.randint(0, NUM_NODES-1),'to': random.randint(0, NUM_NODES-1)} for n in NODE_RAN]
	}
	return model

def _les_mis_example():
	return open(f'{_MYDIR}/graph_les_mis.json').read()

def _manual_example():
	return open(f'{_MYDIR}/graph_small.json').read()

_test_options = {
	'width': 500,
	'height': 500,
	'debug': False,
	'darkMode': True,
	'glowBlend': 0.2,
	'edgeSize': 0.1,
	'fillContainer': True
}

def _tests():
	render_file(_manual_example(), _test_options, 'None', open_file=True)
	render_file(_les_mis_example(), _test_options, 'ForceDirected', open_file=True)
	render_file(_chord_model_example(), _test_options, 'Chord', open_file=True)

if __name__ == '__main__':
	_tests()