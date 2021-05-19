
# using flask_restful
# from flask import Flask, jsonify, request
# from flask_restful import Resource, Api

from myAPIs import utils

PWDICT = {}
TOKENDICT = {}

# utils.init()

# try:
#     with open('passwords.csv') as csv_file:
#        csv_reader = csv.reader(csv_file, delimiter=',')
#        line_count = 0
#        for row in csv_reader:
#           if line_count == 0:
#              # print(f'Column names are {", ".join(row)}')
#              line_count += 1
#           else:
#              # print(f'\t{row[0]} password entry: {row[1]} - {row[2]}.')
#              line_count += 1
#              PWDICT[row[0]] = (row[1], row[2])

#     with open('token.csv') as csv_file:
#        csv_reader = csv.reader(csv_file, delimiter=',')
#        line_count = 0
#        for row in csv_reader:
#           if line_count == 0:
#              # print(f'Column names are {", ".join(row)}')
#              line_count += 1
#           else:
#              # print(f'\t{row[0]} password entry: {row[1]} - {row[2]}.')
#              line_count += 1
#              TOKENDICT[row[0]] = row[1]

# except:
#     print('** error reading pwd or token file - I will continue without it **')