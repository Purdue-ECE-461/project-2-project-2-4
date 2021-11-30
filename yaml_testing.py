import yaml

if __name__ == '__main__':

    stream = open("ECE_461_Fall_2021_Project_2_spec_v1.0.yaml", 'r')
    dictionary = yaml.load(stream)
    for key, value in dictionary.items():
        print (key + " : " + str(value))