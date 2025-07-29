def load_built_in_examples(code_manager):
    """Load updated examples into the code manager."""

    # Example: gr_1 - Student Score Prediction
    gr1_code = '''
import gradio as gr
def pred_score(Gender, pel, lt, tpc, st, ab):
    try:
        input_data = pd.DataFrame({
            'Gender' : [Gender],
            'Parental Education Level' : [pel],
            'Lunch Type' : [lt],
            'Test Preparation Course' : [tpc],
            'Study Time' : [st],
            'Absences' : [ab]
        })

        for col in ending_culm:
            input_data[col] = le[col].transform(input_data[col])

        input_data[sc_culm] = sc.transform(input_data[sc_culm])

        prediction = dt.predict(input_data)
        return f'{prediction[0]:,.2f}'
    except Exception as e:
        return str(e)
gr.Interface(
    fn = pred_score,
    inputs=[
        gr.Dropdown(list(df['Gender'].unique()) , label= 'Gender'),
        gr.Dropdown(list(df['Parental Education Level'].unique()) , label= 'Parental Education Level'),
        gr.Dropdown(list(df['Lunch Type'].unique()) , label= 'Lunch Type'),
        gr.Dropdown(list(df['Test Preparation Course'].unique()) , label= 'Test Preparation Course'),
        gr.Number(label= 'Study Time'),
        gr.Number(label= 'Absences')
    ],

    outputs= gr.Textbox(label= 'The pred score'),
    title= 'Pred Score'
).launch()
'''
    code_manager.save_code("gr_1", gr1_code)

    # Example: gr_2 - House Price Prediction
    gr2_code = '''
import gradio as gr
def predict_house_price(Location, Size, Bedrooms, Bathrooms, YearBuilt, Condition):
  try:
      input_data = pd.DataFrame({
          'Location': [Location],
          'Size (sqft)': [Size],
          'Bedrooms': [Bedrooms],
          'Bathrooms': [Bathrooms],
          'Year Built': [YearBuilt],
          'Condition': [Condition]
      })

      input_data['Location'] = le['Location'].transform(input_data['Location'])
      scaling_cols = ['Size (sqft)', 'Bedrooms', 'Bathrooms', 'Year Built', 'Condition']
      input_data[scaling_cols] = sc.transform(input_data[scaling_cols])
      prediction = rf.predict(input_data)
      return f"Predicted House Price: ${prediction[0]:,.2f}"
  except Exception as e:
      return str(e)
gr.Interface(
    fn=predict_house_price,
    inputs=[
        gr.Dropdown(
            ["Suburban", "Urban", "Rural"], label="Location"),

        gr.Number(label="Size (sqft)"),
        gr.Number(label="Bedrooms"),
        gr.Number(label="Bathrooms"),
        gr.Number(label="Year Built"),
        gr.Number(label="Condition (1-5)")
    ],
    outputs="text",
    title="House Price Prediction"
).launch()
'''
    code_manager.save_code("gr_2", gr2_code)

    # Example: gr_3 - Car Price Prediction
    gr3_code = '''
import gradio as gr
def rel_car_price(Brand, Model_year, Mileage, Fuel_type, Condition, Transmission):
  try:
      input_data = pd.DataFrame({
          'Brand' : [Brand],
          'Model Year' : [Model_year],
          'Mileage (miles)' : [Mileage],
          'Fuel Type' : [Fuel_type],
          'Condition' : [Condition],
          'Transmission' : [Transmission],
      })

      for col in encding_culm:
          input_data[col] = le[col].transform(input_data[col])

      input_data[scaler_colum] = scaler.transform(input_data[scaler_colum])

      prediction = dt.predict(input_data)
      return f'Price ${prediction[0]:,.2f}'
  except Exception as e:
    return str(e)

gr.Interface(
    fn = rel_car_price,
    inputs=[
        gr.Dropdown(['Ford', 'BMW', 'Toyota', 'Honda', 'Chevrolet'], label='Brand'),
        gr.Number(label = 'Model Year'),
        gr.Number(label = 'Mileage (miles)'),
        gr.Dropdown(['Electric' , 'Diesel', 'Gasoline'] , label = 'Fuel Type'),
        gr.Number(label = 'Condition 1 : 5'),
        gr.Dropdown(['Automatic' , 'Manual'] , label = 'Transmission'),
    ],
    outputs= gr.Textbox(label='The pred price'),
    title='Predict car resale'
).launch()
'''
    code_manager.save_code("gr_3", gr3_code)

    # Example: gr_4 - Laptop Price Prediction
    gr4_code = '''
import gradio as gr
def pred_lap_price(Brand, Processor_Type, RAM, Storage, Screen, OS):
    try:
        input_data = pd.DataFrame({
            'Brand': [Brand],
            'Processor Type': [Processor_Type],
            'RAM Size (GB)': [RAM],
            'Storage (GB)': [Storage],
            'Screen Size (inches)': [Screen],
            'Operating System': [OS]
        })

        for col in encding_culm:
            input_data[col] = le[col].transform(input_data[col])

        input_data[scaler_culm] = scaler.transform(input_data[scaler_culm])

        prediction = grid.best_estimator_.predict(input_data)
        return f'${prediction[0]:,.2f}'

    except Exception as e:
        return str(e)

gr.Interface(
    fn = pred_lap_price,
    inputs=[
        gr.Dropdown(choices= list(df['Brand'].unique()) , label='Brand'),
        gr.Dropdown(choices= list(df['Processor Type'].unique()) , label='Processor Type'),
        gr.Number(label='RAM Size (GB)'),
        gr.Number(label='Storage (GB)'),
        gr.Number(label='Screen Size (inches)'),
        gr.Dropdown(choices= list(df['Operating System'].unique()) , label='Operating System')
    ],

    outputs= gr.Textbox(label='The pred price is: '),
    title= 'Pred lap price'
).launch()
'''
    code_manager.save_code("gr_4", gr4_code)

    # Example: gr_5 - College Acceptance Prediction
    gr5_code = '''
import gradio as gr 

def acc_pred(GPA, Ts, Ea, Vh, Rl, Es):
    input_data = pd.DataFrame({
        'GPA' : [GPA],
        'Test Score' : [Ts],
        'Extracurricular Activities' : [Ea],
        'Volunteer Hours' : [Vh],
        'Recommendation Letters' : [Rl],
        'Essay Score' : [Es],
    })
    
    input_data = sc.transform(input_data)
    
    prediction = dt.predict(input_data)
    
    if prediction == 0 : 
        return 'No'
    else:
        return 'Yes'
    
gr.Interface(
    fn= acc_pred,
    inputs=[
        gr.Number(label='GPA'),
        gr.Number(label='Test Score'),
        gr.Number(label='Extracurricular Activities'),
        gr.Number(label='Volunteer Hours'),
        gr.Number(label='Recommendation Letters'),
        gr.Number(label='Essay Score')
    ],
    outputs= gr.Textbox(label= 'The prediction for acceptance: '),
    title= 'Acc pred'
).launch()
'''
    code_manager.save_code("gr_5", gr5_code)

    # Example: gr_6 - Diabetes Prediction
    gr6_code = '''
import gradio as gr 

def diab_pred(age, bmi, bp, pa, fh, ss):
    try:
        input_data = pd.DataFrame({
            'Age' : [age],
            'BMI' : [bmi],
            'Blood Pressure' : [bp],
            'Physical Activity (hours/week)' : [pa],
            'Family History' : [fh],
            'Smoking Status' : [ss]
        })
        
        for col in le_cols:
            input_data[col] = le[col].transform(input_data[col])
            
        input_data[sc_cols] = sc.transform(input_data[sc_cols])    
        
        prediction = rf.predict(input_data)
        
        if prediction == 0:
            return 'No'
        else:
            return 'Yes'
        
    except Exception as e:
        return f'Error {e}'
    
gr.Interface(
    fn = diab_pred,
    inputs= [
        gr.Number(label= 'Age'),
        gr.Number(label= 'BMI'),
        gr.Number(label= 'Blood Pressure'),
        gr.Number(label= 'Physical Activity (hours/week)'),
        gr.Dropdown(choices= list(df['Family History'].unique()) , label= 'Family History'),
        gr.Dropdown(choices= list(df['Smoking Status'].unique()) , label= 'Smoking Status')
        
    ],
    
    outputs= gr.Textbox(label= 'Risk to diabetes'),
    title = 'diab pred'
).launch()
'''
    code_manager.save_code("gr_6", gr6_code)

    # Example: gr_7 - Plant Thrives Prediction
    gr7_code = '''
import gradio as gr 

def pred_ther(st, sl, ws, temp, phl, ps):
    try:
        input_data = pd.DataFrame({
            'Soil Type' : [st],
            'Sunlight (hours/day)' : [sl],
            'Water Supply (liters/week)' : [ws],
            'Temperature (Â°C)' : [temp],
            'pH Level' : [phl],
            'Plant Species' : [ps]
        })
        
        for col in le_cols:
            input_data[col] = le[col].transform(input_data[col])
            
        input_data[sc_cols] = sc.transform(input_data[sc_cols])
        
        prediction = dt.predict(input_data)
        if prediction == 0:
            return 'No'
        else:
            return 'Yes'
    except Exception as e:
        return 'Error {e}'    
    
gr.Interface(
    fn=pred_ther,
    inputs=[
        gr.Dropdown(choices= list(df['Soil Type'].unique()) , label= 'Soil Type'),
        gr.Number(label = 'Sunlight (hours/day)'),
        gr.Number(label = 'Water Supply (liters/week)'),
        gr.Number(label = 'Temperature (Â°C)'),
        gr.Number(label = 'pH Level'),
        gr.Dropdown(choices= list(df['Plant Species'].unique()) , label= 'Plant Species')        
    ],
    outputs= gr.Textbox(label= 'The pred for therives is: '),
    title= 'Therives pred'
).launch()
'''
    code_manager.save_code("gr_7", gr7_code)

    # Example: deb
    deb_code = '''
import gradio as gr
import pandas as pd

def predict(age, bmi, blood_pressure, pa, fh, ss):
    try:
        input_data = pd.DataFrame(
            {
                "": [],  # Fill in column names
            }
        )
        for col in ['', '']:  # Add appropriate column names
            input_data[col] = le[col].transform(input_data[col])

        input_data[scale_cols] = scaler.transform(input_data[scale_cols])

        prediction = dt.predict(input_data)
        if prediction[0] == 1:
            return "Prediction: Positive"
        else:
            return "Prediction: Negative"
    except Exception as e:
        return str(e)

gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Age"),
        gr.Dropdown(choices=['Yes', 'No'], label="Example Dropdown"),
        # Add other inputs here
    ],
    outputs=gr.Textbox(label="Prediction Output")
).launch()
'''
    code_manager.save_code("deb", deb_code)

    # Example: gred
    gred_code = '''
from sklearn.model_selection import GridSearchCV

grid_param = {'max_iter': [23, 35, 50]}  # Define your parameters
grid_search_model = GridSearchCV(lo, grid_param, cv=5)
grid_search_model.fit(x_train, y_train)

print("Best Parameters:", grid_search_model.best_params_)
print("Best Score:", grid_search_model.best_score_)
'''
    code_manager.save_code("gred", gred_code)

    # Example: eval
    eval_code = '''
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Accuracy =", accuracy_score(y_test, y_pred_lo))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_lo))
print("Classification Report:")
print(classification_report(y_test, y_pred_lo))
'''
    code_manager.save_code("eval", eval_code)

    # Example: char
    char_code = '''
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 8))
sns.histplot(df[''], color="Red", kde=True)  # Add column name
plt.title("Distribution of ...")
plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")

plt.figure(figsize=(5, 5))
sns.scatterplot(x=df[''], y=df[''])  # Add column names
plt.title("Scatterplot Title")
plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")
'''
    code_manager.save_code("char", char_code)

    # Example: encode
    encode_code = '''
from sklearn.preprocessing import LabelEncoder

le = {}
for col in encode_cols:  # Add your encode_cols list
    le[col] = LabelEncoder()
    data[col] = le[col].fit_transform(data[col])
'''
    code_manager.save_code("encode", encode_code)

    # Example: scale
    scale_code = '''
from sklearn.preprocessing import StandardScaler

scale_Cols = ['col1', 'col2', 'col3', 'col4', 'col5']  # Replace with your column names
scaler = StandardScaler()
df[scale_Cols] = scaler.fit_transform(df[scale_Cols])

print("Scaled Data:")
print(df[scale_Cols].head())
'''
    code_manager.save_code("scale", scale_code)

    # Example: rscv - Random Search Cross Validation
    rscv_code = '''
from sklearn.model_selection import RandomizedSearchCV
rand_params = {
    'max_depth' : [5, 10, 15, 20, 25],
    'n_estimators' : [100, 200, 300, 400, 500]
}

random_model = RandomizedSearchCV(rf , rand_params, cv=5)
random_model.fit(x_train , y_train)
print('Best params for rand model: ', random_model.best_params_)

y_pred_rand = random_model.best_estimator_.predict(x_test)
print('MAE for rand model: ' , mean_absolute_error(y_test , y_pred_rand))
print('MSE for rand model: ' , mean_squared_error(y_test , y_pred_rand))
print('R2 for rand model: ' , r2_score(y_test , y_pred_rand))
'''
    code_manager.save_code("rscv", rscv_code)

    # Example: gscv - Grid Search Cross Validation
    gscv_code = '''
from sklearn.model_selection import GridSearchCV

grid_params = {
    'max_depth' : [5, 10, 15, 20, 25],
    'max_leaf_nodes' : [5, 10, 15, 20, 25]
}
grid_model = GridSearchCV(dt, grid_params, cv=5)
grid_model.fit(x_train , y_train)
print('Best params' , grid_model.best_params_)
y_pred_grid = grid_model.best_estimator_.predict(x_test)

print('Accuracy score for grid model is: ' , accuracy_score(y_test , y_pred_grid))
'''
    code_manager.save_code("gscv", gscv_code)

    # Example: le - Label Encoding
    le_code = '''
le = {}
encding_culm = ['']  # Add your categorical columns here
for col in encding_culm:
    le[col] = LabelEncoder()
    df[col] = le[col].fit_transform(df[col])
print(le)
'''
    code_manager.save_code("le", le_code)

    # Example: sc - MinMax Scaling
    sc_code = '''
sc = MinMaxScaler()
sc_culm = []  # Add your numerical columns here
df[sc_culm] = sc.fit_transform(df[sc_culm])
'''
    code_manager.save_code("sc", sc_code)
