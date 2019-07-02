# -*- coding: utf-8 -*-


import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException

import os
from pprint import pprint
import json
from textblob import TextBlob

import pandas as pd

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username='8c802d3b-1dcd-4bec-97d3-caf2d9453d3e',
    password='fOi2JdeijbAB',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

classes = ['english']

onlyfiles = [[], []]
columns = None
all_data = []

def read_file():
	for c in range(len(classes)):
		cls = classes[c]
		datapath = './'+cls+'/'
		for datafile in os.listdir(datapath):
			if datafile[0]=='.':
				continue
			filename = os.path.join(datapath, datafile)
			if(os.path.isfile(filename)):
				# print(filename)
				onlyfiles[c].append(filename)
			else:
				print('?')

	print(len(onlyfiles[0]))
	print(len(onlyfiles[1]))

	for c in range(len(classes)):
		cls = classes[c]
		for fn in onlyfiles[c]:
			print(fn)
			with open(fn, 'r') as ins:
				data = []
				for line in ins:
					data.append(line)
				# pprint(data)
				headline = data[0]
				text = ''
				for lidx in range(0, len(data)):
					text += data[lidx]
				print(headline)
				print(text)
				tone_analyze(headline, text, cls, fn)

def tone_analyze(headline, text, cls, fn):
	try:
		text = ''.join([i if ord(i) < 128 else ' ' for i in text])
		tone_analysis = tone_analyzer.tone(
	    	{'text': text},
	    	'application/json')
		# output = json.dumps(tone_analysis, indent=2)
		filename = fn[:-4]+'_output'+fn[-4:]
		json.dump(tone_analysis, open(filename, 'w'))
		pre_process(headline, cls, filename)		
	except WatsonApiException as ex:
	    print "Method failed with status code " + str(ex.code) + ": " + ex.message



def pre_process(headline, cls, filename):
	global columns
	output = json.load(open(filename))

	pprint(output.keys())

	# pprint(output['document_tone'])

	tone_names = ['Analytical', 'Confident', 'Tentative',
				'Anger', 'Joy', 'Sadness', 'Fear', 'Disgust',
				'Agreeableness', 'Conscientiousness', 'Emotion Range', 'Extraversion', 'Openness']


	column_names = ['headline_Subjectivity', 'headline_Polarity']
	for key in output.keys():
		for tone in tone_names:
			column_names.append(key+'_'+tone)
	column_names.append('sentences_count')
	column_names.append('class')
	print(len(column_names))
	columns = column_names
	print(columns)

	row = []
	try:
		headline_sentiment_analysis = TextBlob(headline)
		row.append(headline_sentiment_analysis.sentiment.subjectivity)
		row.append(headline_sentiment_analysis.sentiment.polarity)
	except:
		row.append(0)
		row.append(0)

	for key in output.keys():
		if key=='document_tone':
			data = output['document_tone']['tones']
			# pprint(data)
			tone_dict = {}
			for entry in data:
				if entry['tone_name'] not in tone_dict.keys():
					tone_dict[entry['tone_name']] = entry['score']
				else:
					tone_dict[entry['tone_name']] += entry['score']
			for tone_name in tone_names:
				# print(tone_name)
				if tone_name in tone_dict.keys():
					score = tone_dict[tone_name]
				else:
					score = 0
				row.append(score)

		if key=='sentences_tone':
			tone_dict = {}
			for sentence_idx in range(len(output['sentences_tone'])):
				sentence = output['sentences_tone'][sentence_idx]
				data = sentence['tones']
				# pprint(data)
				for entry in data:
					if entry['tone_name'] not in tone_dict.keys():
						tone_dict[entry['tone_name']] = entry['score']
					else:
						tone_dict[entry['tone_name']] += entry['score']
			for tone_name in tone_names:
				# print(tone_name)
				if tone_name in tone_dict.keys():
					score = tone_dict[tone_name]
				else:
					score = 0
				row.append(score)
			row.append(len(output['sentences_tone']))
			row.append(cls)
	print(len(row))
	all_data.append(row)

read_file()
df = pd.DataFrame(all_data, columns = columns)
df.to_csv('bengali_satire_tone_data_run_4.csv')
