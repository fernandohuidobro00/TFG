
from deepcarskit.quick_start import  load_data_and_model
import torch

#path = '/home/fernando/Escritorio/TFG/DeepCARSKit/saved/NeuCMFii-Apr-04-2023_18-39-21_f1.pth'
path_model = '/home/fernando/Escritorio/TFG/DeepCARSKit/saved/NeuCMFii-Apr-25-2023_10-19-48_f1.pth'

path_dataset = '/home/fernando/Escritorio/TFG/DeepCARSKit/saved/yelp-dataset.pth'
path_dataloader = '/home/fernando/Escritorio/TFG/DeepCARSKit/saved/yelp-for-NeuCMFii-dataloader.pth'


config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        dataset_file=path_dataset,
        model_file=path_model,
        #dataloader_file=path_dataloader,
    )



print(dataset)  
print(model.type)
print(model.device)
#print(model.predict)




# example of predictions by context recommender
# note, raw value in the original data is expected to be transformed to inner ID

# rawid <--->innderid
print("innerid: ", dataset._get_innerid_from_rawid("user_id", "3LMZ79mM8jGLMyCa6-D4nw"))
print("rawid: ", dataset._get_rawid_from_innerid("user_id", 1))

userid = dataset._get_innerid_from_rawid("user_id","22Y8hc4NYWPa2D6ffodddg")
business_id = dataset._get_innerid_from_rawid("business_id","9fjdQvNl1yWKCNgo0VaCyA")
day_id = dataset._get_innerid_from_rawid("day","WE")
hour_day = dataset._get_innerid_from_rawid("hour","Din")
category_id = dataset._get_innerid_from_rawid("categories","7-8")
popular_id = dataset._get_innerid_from_rawid("popular","NoPop")
parking_id = dataset._get_innerid_from_rawid("parking","NoGar")


user = torch.tensor([userid]).to(model.device)
business = torch.tensor([business_id]).to(model.device)
contexts = []
contexts.append(torch.tensor([day_id]).to(model.device))
contexts.append(torch.tensor([hour_day]).to(model.device))
contexts.append(torch.tensor([category_id]).to(model.device))
contexts.append(torch.tensor([popular_id]).to(model.device))
contexts.append(torch.tensor([parking_id]).to(model.device))

#user_id:token,review_id:token,rating:float,day:token,hour:token,categories:token,popular:token,parking:token,contexts:token,uc_id:token

print(user)
prediction = model.forward(user, business, contexts)
print(prediction)

item = prediction.item()
print(item)
#print("prediction: ",model.forward(user, business, contexts))

#print(dir(model.forward(user, business, contexts)))
