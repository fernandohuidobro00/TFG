
from deepcarskit.quick_start import  load_data_and_model
import torch
import json
import copy
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



# id = 1

# user_ids = ['22Y8hc4NYWPa2D6ffodddg','qibGLHABNReGeJr2w4_8yQ', 'GmpSEv4b0AoIFATqNBu1bQ',
# 			'iC5JO52dGKJNxfzp3OVLPw','Zn8tgekH0oCfyk4SUtygoA','ez24d08Qyqb7mCKEuTaifQ']

# business_ids = ['tjEKEDmyR_VmeBkJGwreLA', 'BEMSDLPP630Fpdw_QpqLVA', '7BI3i_-l9VZwycB7ovMn6w', 'mIwPIJqIqAaDVZHJTtodbA', 'Eg1k3utDrdi5qyzVbw9xyQ' 
# 			, 'WQ832PDnsDshhbQFm83ISg','ROnkVXPz5jRlMQvLw05UEA', '3WC9HidyqFisiDxP1dcFCA'
# 			, '5YLYDvCXsHiQW4VHOFMEfg', 'yrwoDu4AqkqbaLhTtFTFEw'] 



# print("innerid: ", dataset._get_innerid_from_rawid("user_id", "3LMZ79mM8jGLMyCa6-D4nw"))
# print("rawid: ", dataset._get_rawid_from_innerid("user_id", 1))



list_dict = []

business_ids = ['mYMPepp0QIZRk_52pWzeoA','JzQsy7_G0p-UZGYFMCEHvQ', 'o_5z2Qt335Or-TTnECOIiw', 'KhBUg5QhBYuK8RZAe5gDMQ', 
                'BGc_EYORXo9O9A9IQ2MkxA', 'sPy8XUOJ0ax5Zh2yEsl4cA', 'c_4c5rJECZSfNgFj7frwHQ', 
                'vWRdL8B9o2CmUmfJgNgMqQ', 'HgPTy_OGoaxllb2EXkC1sQ', 'n_7EQxn0ciucIOJfpWVaTQ']


new_user_ids = [ 'RwPKUrc0ae54hV1DWU1MsQ', 'I2XpWCHAom1JRyHXZQrnfg',
                  'vffKQc_WQMYFGY4JS5VAOw', 'AaJ9d4OrFmgc4S_U2QiSZg', 'pou3BbKsIozfH50rxmnMew', 'fr1Hz2acAb3OaL3l6DyKNg']


with open("/home/fernando/Escritorio/TFG/DeepCARSKit/dataset/yelp/yelp.inter", "r") as archivo:
    lineas = archivo.readlines()  # leer todas las líneas en una lista

    # Omitir la primera línea utilizando slicing
    lineas_sin_primera = lineas[1:]

    # Procesar las líneas sin la primera
    for linea in lineas_sin_primera:
        dict_user = {}
        datos = linea.split(",")
        us = datos[0]
        if us in new_user_ids:
            bus = datos[1]
            if bus in business_ids:
                categories = datos[5]
                popular = datos[6]
                parking = datos[7]
                # Comprobar si ya existe un diccionario con la misma clave y el mismo business
                if any(d.get(us, {}).get('business') == bus for d in list_dict):
                    continue  # Si ya existe, no se agrega un nuevo diccionario a la lista
                dict_user[us] = {'business': bus, 'categories': categories, 'popular': popular, 'parking': parking}
                list_dict.append(dict_user)

new_dic_results = []


for d in list_dict:
    key_user =  list(d.keys())[0]
    dic_business = d[key_user]['business']
    dic_category = d[key_user]['categories']
    dic_popular = d[key_user]['popular']
    dic_parking = d[key_user]['parking']

    userid = dataset._get_innerid_from_rawid("user_id",key_user)
    business_id = dataset._get_innerid_from_rawid("business_id",dic_business)
    category_id = dataset._get_innerid_from_rawid("categories",dic_category)
    popular_id = dataset._get_innerid_from_rawid("popular",dic_popular)
    parking_id = dataset._get_innerid_from_rawid("parking",dic_parking)
   

    day_list = ["WE","WD"]
    hour_list = ["Din","Lch"]

    for da in day_list:
        for h in hour_list:
            print(da)
            print(h)
            day_id = dataset._get_innerid_from_rawid("day",da)
            hour_day = dataset._get_innerid_from_rawid("hour",h)          
            user = None
            business=None
            user = torch.tensor([userid]).to(model.device)
            business = torch.tensor([business_id]).to(model.device)
            contexts = []
            contexts.append(torch.tensor([day_id]).to(model.device))
            contexts.append(torch.tensor([hour_day]).to(model.device))
            contexts.append(torch.tensor([category_id]).to(model.device))
            contexts.append(torch.tensor([popular_id]).to(model.device))
            contexts.append(torch.tensor([parking_id]).to(model.device))


            prediction = model.forward(user, business, contexts)

            d_copy = copy.deepcopy(d)
            key_user = list(d_copy.keys())[0]

            item = prediction.item()
            d_copy[key_user]['day'] = da
            d_copy[key_user]['hour'] = h

            d_copy[key_user]['predic'] = item
            new_dic_results.append(d_copy)


route = '/home/fernando/Escritorio/TFG/proyect/dic_information.json'
file = open(route,"w")
for d in new_dic_results:
    jason = json.dump(d,file)
    file.write("\n")

file.close()



#print("prediction: ",model.forward(user, business, contexts))

#print(dir(model.forward(user, business, contexts)))
