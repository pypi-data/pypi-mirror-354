from ml_determination.predict_matrix_language import MatrixLanguageDeterminerP12

model_path = '/home/acq21oi/projects/ml_determination_lms/ml-determination-lms'
ml = MatrixLanguageDeterminerP12(
    L1='ZH', L2='EN',
    config={
        'EN': {
            'data_path': model_path + '/en/',
            'model_path': model_path + '/en/model.pt'},
        'ZH': {
            'data_path': model_path + '/zh/',
            'model_path': model_path + '/zh/model.pt'}},
    alpha=1.2765)
print(ml.determine_ML('然后 那些 air supply 的 然后 michael learns to rock 的 啊 certain 的 啦'))