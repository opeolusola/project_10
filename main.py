import os, pandas as pd, numpy as np, json


if __name__ == "__main__":
    csv_fol = os.path.join(os.getcwd(),'260821')
    csv_names = os.listdir(csv_fol)

    # get static tables into a dataframe 
    store_details = pd.read_csv("Stores.csv")
    product_details = pd.read_csv("Product.csv")

    #Data Manipulation 1. Loop through allcsvs file and combine to one master file
    all_data = pd.DataFrame([])
    for csv_file in csv_names:
        df_csv= pd.read_csv(os.path.join(csv_fol,csv_file))
        all_data =all_data.append(df_csv)

    all_data.to_dict()


    #Data Manipulation 2: categorize each transaction by total sales.
    #Condition: If sales is lower than 100, Low Sale
    #If sales is between 100 and 300, Medium Sale
    #If sales is greater than 300, High Sale

    conditions = [  (all_data['Total_Sales'] < 100),(all_data['Total_Sales'] >= 100)]
    values = ["Low Sale","High Sale"]
    all_data['Total_Sales_Category'] = np.select(conditions, values)

  
    #Data Manipulation 3: do a look up to stores table to bring in store name for every transaction
    #the function below returns store name for a specified store id
    def getStoreName(storeid, df_name ):
        store_name = df_name.loc[df_name['Store_Id']== storeid, 'Name']
        return store_name


    #do a look up to product table to bring in product name for every transaction
    #the function below returns product name for a specified product id
    def getProductName(productid, df_name ):
        product_name = df_name.loc[df_name['Product_id']== productid, 'Name']
        return product_name


    #create empty lists (store_names and product_names) 
    # where store name and product name for each transaction will be populated respectively
    store_names =[]
    product_names = []
    for index , row in all_data.iterrows():
        store_id = row["Store_Id"]
        product_id = row["Product_id"]
        store_names.append(getStoreName(store_id,store_details))
        product_names.append(getProductName(product_id, product_details))

    #create new columns in the all_data called store_names and product_names
    all_data["Store_Name"]=store_names
    all_data["Product_Name"]=product_names


    #create a new column that applies 10% discount to Total_Sales
    all_data["Sales_after_discount"]= all_data["Total_Sales"] * 0.9

    #save all_data to csv format
    all_data.to_csv("Sales_Records.csv")

    #save all_data to json format
    all_data_json  = all_data.to_json(orient="records")
    parsed = json.loads(all_data_json)
    print(json.dumps(parsed, indent=4))

 






    


