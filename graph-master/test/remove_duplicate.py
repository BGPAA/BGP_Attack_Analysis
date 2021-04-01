#!/usr/bin/env python
# coding: utf-8

import os
import json

#os.system('cp toto.json reduct.all.hijacks.json')

file = open("toto.json", "r")
dico = []
for i, v in enumerate(file):
    dico.append([i, v])

file.close()

json_field_values = []
for i in range(0, len(dico) - 1):
    first_step_transformed_current_line = dico[i][1].replace('{', '').replace('}', '')
    first_step_transformed_current_line = first_step_transformed_current_line.split(',')
    second_step_transformed_current_line = (first_step_transformed_current_line[5].split(' '))[2]
    json_field_values.append(second_step_transformed_current_line)

print(json_field_values)

i = 0
while(i != len(json_field_values) - 1): 
    j = i + 1
    while(j != len(json_field_values) - 0):
        if (json_field_values[i] == json_field_values[j]):
            json_field_values.remove(json_field_values[j])
            dico.remove(dico[j])
        else:
            j += 1
    if(i == len(json_field_values) - 1):
        break
    else:
        i += 1

file = open("reduct.json", "w")

for el in dico:
    file.write(el[1])

file.close()
