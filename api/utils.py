import json
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from flask import render_template

def initialize():        
    config = {}
    with open('config.json') as f:
        c= json.load(f)
        config['tmp_dir'] = c['tmp_dir']        
        if not os.path.isdir(config['tmp_dir']):
            os.mkdir(config['tmp_dir'])

        config['img_size'] = (c['img_size'], c['img_size'])
        config['classes'] = c['classes']
        config['models'] = {}
        for m in c['models']:
            config['models'][m] = keras.models.load_model(c['models'][m])
    return config

def load_image(path, config):
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img)
    img = tf.image.resize(img, size=config['img_size'])
    return img

def evaluate_image(path, config, metric, top_k, options):
    img = load_image(path, config)
    result = config['models'][metric].predict(tf.expand_dims(img, axis=0))
    result_id = np.argsort(result)[0, ::-1][:top_k]
    retVal =[]    
    
    for i, r in enumerate(result_id):
        curr = {}
        curr['rank'] = str(i)
        if options['id']:
            curr['id'] = str(r)
        if options['name']:
            curr['name'] = config['classes'][r]
        if options['probability']:
            curr['probability'] = '{:.8f}'.format(result[0, r])
        retVal.append(curr)
    return retVal

def handle_get():    
    return render_template('upload.html')

def handle_post(request, config):
    top_n = int(request.form.get('top_n'))
    metric = request.form.get('metric')
    options = {
        'id': True if request.form.get('option_id') == 'on' else False,
        'name': True if request.form.get('option_name') == 'on' else False,
        'probability': True if request.form.get('option_probability') =='on' else False
    }
    
    f = request.files['file']
    retVal = '0'
    if len(f.filename) > 0:
        tmp_path = config['tmp_dir'] + f.filename
        f.save(tmp_path)
        retVal = evaluate_image(tmp_path, config, metric, top_n, options)
        os.remove(tmp_path)
    
    return {
    #    'top_n': str(top_n),
    #    'metric': metric,
    #    'options': options,
        'predictions': retVal
    }