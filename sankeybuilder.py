import pandas as pd
import dash
import plotly.graph_objects as go

app = dash.Dash()



scenario = '2050_high_demand' #input("Enter scenario then press enter: ") 
iteration = 'Run_6_7_' #input("Enter iteration number then press enter: ")


df = pd.read_csv('dummy_sankey2.csv')

df = df[(df['scenario'] == scenario) & (df['iteration'] == iteration)]
df.head()
df = df[df['input'].str.contains('elec_lines') == False]
df = df[df['input'].str.contains('Hydrogen refueller') == False]
df = df[df['input'].str.contains('substation') == False]
df = df[df['input'].str.contains('mileage') == False]
df = df[df['output'].str.contains('mileage') == False]
df = df[df['input'].str.contains('transport') == False]
df = df[df['input'].str.contains('Biomass import') == False]
df = df[df['input'].str.contains('export') == False]
df = df[df['output'].str.contains('elec_lines') == False]
df = df[df['output'].str.contains('substation') == False]


df.loc[(df['input']=='Primary electricity'), 'input'] = 'Electricity'
df.loc[(df['output']=='Hydrogen refueller'), 'output'] = 'Hydrogen refueller to transport'
df.loc[(df['output']=='Primary electricity'), 'output'] = 'Electricity'
df.loc[(df['input']=='Grid electricity'), 'input'] = 'Electricity'
df.loc[(df['output']=='Grid electricity'), 'output'] = 'Electricity'
df.loc[(df['output']=='Grid electricity'), 'output'] = 'Electricity'






colour_dict = {
    'Anaerobic digestion':'#808080',
    'Battery':'#7f0000',
    'Biomass':'#006400',
    'Hydrogen':'#808000',
    'Boiler':'#808000',
    'Electricity':'#483d8b',
    'Biomass boiler to electricity':'#3cb371',
    'Biomass boiler to heat':'#008080',
    'Heat':'#000080',
    'Heat demand':'#4682b4',
    'Electricity transport':'#cd853f',
    'Petrol/diesel':'#cd853f',
    'Electricity demand':'#7e7a36',
    'Hydrogen heat demand':'#32cd32',
    'Industrial hydrogen demand':'#8b008b',
    'Electrolyser':'#b03060',
    'EV chargers':'#d2b48c',
    'Bioenergy and waste':'#d2b48c',
    'Ground PV':'#ff4500',
    'Heat network':'#00ff00',
    'Heat pump':'#00ced1',
    'Hydroelectricity':'#ff8c00',
    'Hydrogen CCGT':'#ffd700',
    'Oil/solid/coal':'#ffd700',
    'Hydrogen OCGT':'#0000ff',
    'Hydrogen boiler to heat':'#a020f0',
    'Transport demand':'#a020f0',
    'Hydrogen CHP':'#f08080',
    'Gas boiler':'#f08080',
    'Hydrogen export':'#adff2f',
    'Hydrogen import':'#dc143c',
    'Natural gas':'#dc143c',
    'Hydrogen refueller to transport':'#b0c4de',
    'Road vehicles':'#b0c4de',
    'Hydrogen storage tank':'#f0e68c',
    'Hydrogen transport':'#1e90ff',
    'National grid export':'#ff00ff',
    'National grid import':'#d6f0ef',
    'Onshore wind':'#98fb98',
    'Resistance heating':'#7b68ee',
    'Rail':'#7b68ee',
    'Rooftop PV':'#ee82ee',
    'Sewage gas':'#98fb98',
    'Solar thermal':'#7fffd4',
    'Hydrogen heat':'#f0e68c',
    'Landfill gas':'#ffc0cb'
}

def assign_colour(label_input):
    for label, colour in colour_dict.items():
        if label == label_input:
            return colour



def get_sankey(data,path,value_col):
    sankey_data = {
    'label': [],
    'source': [],
    'target' : [],
    'value' : []

    }
    counter = 0
    while (counter < len(path) - 1):
        for parent in data[path[counter]].unique():
            sankey_data['label'].append(parent)
            for inputs in data[data[path[counter]] == parent][path[counter]].unique():
                for outputs in data[data[path[counter]] == parent][path[counter+1]]:
                    weights = data[(data[path[counter+1]] == outputs) & (data[path[counter]] == inputs)][value_col].sum()
                    sankey_data['label'].append(outputs)
                    sankey_data['source'].append(sankey_data['label'].index(parent))
                    sankey_data['target'].append(sankey_data['label'].index(outputs))
                    sankey_data['value'].append(round(float(weights)))
        counter +=1
    return sankey_data





my_sankey = get_sankey(df, ['input','output'],'weight')

#add weight value to labels and assign colours
label_vals = ["Electricity","Battery"]
colours_list = []
for i in my_sankey['label']:
    colours_list.append(assign_colour(i))
    if i in df['input'].values:
        temp = df[df['input']==i]['weight'].sum()
        label_vals.append(i+ ": "+str(round(float(temp))))
    elif i in df['output'].values:
        temp = df[df['output']==i]['weight'].sum()
        label_vals.append(i+ ": "+str(round(float(temp))))



fig = go.Figure(data=[go.Sankey(
    arrangement="perpendicular", #other layout options available
    node = dict(
      pad = 30, #spacing between nodes
      thickness = 15,#thickness of nodes
      line = dict(color = "black", width = 0.5), #node outline
      label = label_vals,
      color = "red" #change this to a given colour for them to be monochromatic or to label_colours for random colours
    ),
    link = dict(
      source = [0],
      target = [1],
      value = [7111456.016]
  ))])
fig.update_layout(height=1150, width=1500, margin={'t':150,'b':20,'l':10,'r':150}, font= dict(size=25))
fig.show()






