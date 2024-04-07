from recbole.quick_start import run_recbole


run_recbole(
   model='DeepFM', 
   dataset='BasketRecommendation',
   config_file_list=[
       'DeepFM.yaml'
       ],
   )