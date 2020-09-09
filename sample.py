from ChromaCqt import ChromaCqt

#実装サンプル
al1=ChromaCqt()
al1.load_music('file.wav')
#al1.cut(al1.loaded_data,7,56)
#al1.lr_separate(al1.cut_data)
al1.lr_separate(al1.loaded_data)
al1.hpss_execute(al1.lr_separated_data,'right')
al1.chromacqt_execute(al1.hpss_data['harmonic'])

print(al1.chrcqt_data)
al1.disp_chrcqt(al1.chrcqt_data)
al1.export_csv()
