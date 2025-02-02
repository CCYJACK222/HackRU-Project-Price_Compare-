import pandas as pd

# Read the CSV file
df = pd.read_csv('rutgers_university_supermarkets.csv')

# Drop the 'Supermarket Address' column
df = df.drop(['Supermarket Address'], axis=1)
df = df.drop(['University'], axis=1)


# Split the 'Supermarket Coordinates' into two new columns: 'Latitude' and 'Longitude'
df[['Latitude', 'Longitude']] = df['Supermarket Coordinates'].str.split(',', expand=True)

# Clean up any extra spaces in the columns
df['Latitude'] = df['Latitude'].str.extract('([0-9.-]+)')[0]
df['Longitude'] = df['Longitude'].str.extract('([0-9.-]+)')[0]

# Drop the original 'Supermarket Coordinates' column
df = df.drop(['Supermarket Coordinates'], axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_rutgers_university_supermarkets.csv', index=False)

