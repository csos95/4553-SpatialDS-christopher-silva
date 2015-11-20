"""
@author - Christopher Silva
@date -  11/20/2015
@description - This program loads the nodes, edges, and geometry files so
that they can be using in other programs
"""
import csv
import json

print ('Christopher Silva\nProgram 5 - Part 1\n')

nodes =[]
edges = []
geometry = {}

with open('nodes.csv', 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in rows:
        nodes.append(row)
    print ('nodes.csv read containing ',len(nodes),' nodes.')
    
with open('edges.csv', 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in rows:
        edges.append(row)
    print ('edges.csv read containing ',len(edges),' edges.\n')

f = open('nodegeometry.json', 'r')

for line in f:
    line = json.loads(line)
    #use json.loads on line['geometry'] so that the value for the node id is a list
    #instead of a string
    geometry[line['id']] = json.loads(line['geometry'])

print ('Node 202451 contains ',len(geometry['202451']),' points. The geometry follows:\n')
for point in geometry['202451']:
    print(point)