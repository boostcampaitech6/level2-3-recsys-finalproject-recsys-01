from recbole.quick_start import run_recbole

run_recbole(
   model='BERT4Rec', # GRU4Rec, SASRec, BERT4Rec
   dataset='BasketRecommendation', 
   config_file_list=[
       'seq-train-config.yaml'
       ],
   )
