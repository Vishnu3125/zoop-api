from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from fuzzywuzzy import fuzz

app = FastAPI()

class vehicalDetails(BaseModel):
    """ Query Parameters schema """
    make: str
    modelVariant: str
    fuel: str
    seatingCapacity : int


df = pd.read_excel('dataset.xlsx')
df = df.drop(["_id"], axis=1)

@app.post("/queryData")
async def queryData(vDetails: vehicalDetails):
    filteredData = df.loc[(df['fuel'] == vDetails.fuel) & (df['seatingCapacity'] == vDetails.seatingCapacity)]
    filteredData = filteredData.values.tolist()

    if any(filteredData):
        output = []
        for row in filteredData:
            makeMatch = fuzz.ratio(str(row[0]), vDetails.make)
            modelMatch = fuzz.ratio(str(row[1]), vDetails.modelVariant)
            variantMatch = fuzz.ratio(str(row[2]), vDetails.modelVariant)
            output.append((makeMatch + modelMatch + variantMatch) / 3)

        score = max(output)
        result = filteredData[output.index(score)]
        return {
            "make" : result[0],
            "model" : result[1],
            "variant" : result[2],
            "fuel" : result[3],
            "seatingCapacity" : result[4],
            "Score" : score
        }
    else:
        return []