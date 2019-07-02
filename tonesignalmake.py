import json
from pprint import pprint
from numpy import array, ones
import numpy
from scipy.ndimage import gaussian_filter
from matplotlib.pyplot import *
from os import listdir

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 25})
plt.locator_params(axis = 'x', numticks = 5)
plt.locator_params(axis = 'y', nbins = 6)

M = 3

xs = {'g':[], 'r': []}
ys = {'g':[], 'r': []}
zs = {'g':[], 'r': []}

fign = 'Confident'

def tone_graph(filename):
    print(filename)
    with open(filename, 'r') as fp:
        all_data = json.load(fp)

    #pprint(all_data)
    emotions = {'Analytical':[], 'Confident':[], 'Tentative':[],
        'Anger':[], 'Joy':[], 'Sadness':[], 'Fear':[], 'Disgust':[],
        'Agreeableness':[], 'Conscientiousness':[], 'Emotion Range':[], 'Extraversion':[], 'Openness':[]}

    # print(len(all_data['sentences_tone']))
    data = all_data['document_tone']['tones']
    #pprint(data)
    #print()
    #print(type(data))
    if (len(data)==0):
        for k in emotions.keys():
            emotions[k].append(0.0)
    else:
        entry_emos = {'Analytical':0, 'Confident':0, 'Tentative':0,
                      'Anger':0, 'Joy':0, 'Sadness':0, 'Fear':0, 'Disgust':0,
                      'Agreeableness':0, 'Conscientiousness':0, 'Emotion Range':0, 'Extraversion':0, 'Openness':0}
        for entry in data:
            #print(entry['tone_name'])
            if entry['tone_name'] not in entry_emos.keys():
                entry_emos[entry['tone_name']] = entry['score']
                #print(entry_emos[entry['tone_name']])
            else:
                entry_emos[entry['tone_name']] += entry['score']
                #print(entry_emos[entry['tone_name']])

        for k in emotions.keys():
            emotions[k].append(entry_emos[k])
    if 'sentences_tone' in all_data.keys():
        for sentence_idx in range(len(all_data['sentences_tone'])):
            sentence = all_data['sentences_tone'][sentence_idx]
            data = sentence['tones']
            #pprint(data)
            #print()
            #print(type(data))
            if (len(data)==0):
                for k in emotions.keys():
                    emotions[k].append(0.0)
            else:
                entry_emos = {'Analytical':0, 'Confident':0, 'Tentative':0,
                              'Anger':0, 'Joy':0, 'Sadness':0, 'Fear':0, 'Disgust':0,
                              'Agreeableness':0, 'Conscientiousness':0, 'Emotion Range':0, 'Extraversion':0, 'Openness':0}
                for entry in data:
                    #print(entry['tone_name'])
                    if entry['tone_name'] not in entry_emos.keys():
                        entry_emos[entry['tone_name']] = entry['score']
                        #print(entry_emos[entry['tone_name']])
                    else:
                        entry_emos[entry['tone_name']] += entry['score']
                        #print(entry_emos[entry['tone_name']])

                for k in emotions.keys():
                    emotions[k].append(entry_emos[k])

    pprint(len(emotions['Joy']))
    pprint(len(emotions['Confident']))

    
    x = array(emotions[fign])
    # print(emotions['Analytical'])

    def smooth(x,window_len=M,window='hanning'):
        s=numpy.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
        #print(len(s))
        if window == 'flat': #moving average
            w=numpy.ones(window_len,'d')
        else:
            w=eval('numpy.'+window+'(window_len)')

        y=numpy.convolve(w/w.sum(),s,mode='valid')
        return y



    def rescale(arr):
        n = len(arr)
        return np.interp(np.linspace(0, 50), np.arange(n), arr)



    y = smooth(x)
    print(y)

    z = gaussian_filter(x, sigma = 5, mode = 'reflect')

    # x = rescale(x)
    # y = rescale(y)
    # z = rescale(z)

    if(y.shape[0]>=25):
        x = rescale(x)
        y = rescale(y)
        z = rescale(z)
        if cls=='Satire':
            xs['g'].append(x)
            ys['g'].append(y)
            zs['g'].append(z)
        elif cls=='Fake':
            xs['r'].append(x)
            ys['r'].append(y)
            zs['r'].append(z)


# filename = './Fake/123_output.txt'
classes = ['Fake', 'Satire']

for cls in classes:
    folder = './'+cls+'/'
    datafiles = []
    for f in listdir(folder):
        if f.endswith('_output.txt'):
            filename = folder+f
            datafiles.append(filename)
            tone_graph(filename)

# f, axes = plt.subplots()
# axes.set_xlim([0, 50])
# axes.set_ylim([0, 1])
# axes.set_yticks([0, 0.25, 0.50])
# fig, axarr = subplots(1, 2, sharey = True, figsize=(15, 5))
print('*******************************')
line_types = {'g':'', 'r': '--'}
for i, col in enumerate(['g', 'r']):
    # figure(col)
    # for z in ys[col]:
    #     plot(z, col)
    plot(np.mean(ys[col], axis = 0), col+line_types[col], linewidth=3.5)
    savefig('LaTeX/figures/'+fign.lower()+'.png')
    print()
    # axarr[i].plot(np.mean(ys[col], axis = 0), col)

show()