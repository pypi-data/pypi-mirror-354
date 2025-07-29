import itertools

import tensorflow as tf

# METADATA ####################################################################

def _label(c: str) -> str:
    return '#{}'.format(c.encode('utf-32-be').hex())

def label(token: str) -> str:
    return ' '.join(_label(__c) for __c in token)

# SERIALIZATION ###############################################################

def write(data: any, path: str, tsv: bool=True) -> None:
    with open(path, 'w') as __f:
        for __row in data:
            __line = '\t'.join(str(__v) for __v in __row) if tsv else repr(__row)[1:-1]
            __f.write(__line + '\n') # escape special characters

# STATS #######################################################################

def stats(dataset: tf.data.Dataset, count: int=None, features: list=[]) -> dict:
    # init
    __min, __avg, __max, __cnt = 0, 0, 0, 0
    # scan the whole dataset
    for __sample in itertools.islice(dataset, 0, count):
        # preprocess
        __s = tf.strings.join(inputs=[__sample[__f] for __f in features], separator='\x1d').numpy() if features else __sample.numpy()
        __l = len(__s)
        # compute
        __min = min(__min, __l)
        __max = max(__max, __l)
        __avg = __avg + __l
        __cnt = __cnt + 1
    # average
    __avg = __avg // __cnt
    # format
    return {'min': __min, 'avg': __avg, 'max': __max}

# PIPELINE ####################################################################

def process(dataset: tf.data.Dataset, pipeline: list, replace: bool=True) -> tf.data.Dataset:
    __dataset = dataset
    # specify how to combine each operation result with the original dataset
    __replace = len(list(pipeline)) * [replace] if isinstance(replace, bool) else replace
    # apply the operation successively
    for __fn, __repl in zip(pipeline, __replace):
        __new = __dataset.map(__fn)
        __dataset = __new if __repl else __dataset.concatenate(__new)
    return __dataset
