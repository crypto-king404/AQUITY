const express = require("express");
const mongoose = require("mongoose");
const app = express();
const port = 4000; // Choose your desired port

// Connect to your MongoDB database
mongoose.connect("mongodb+srv://<username>:<password>@waterviewcluster.djdmxsj.mongodb.net/?retryWrites=true&w=majority", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  dbName: "your-database-name",
});

// Define a schema and model for your data
const dataSchema = new mongoose.Schema({
  site_no: Number,
  datetime: Date,
  "Mean Water Temp (C)": Number,
  "Mean Specific Conductance": Number,
  "Turbidity (FNU)": Number,
  pH: Number,
});

const DataModel = mongoose.model("Data", dataSchema);

// API route to get the old and new data
app.get("/api/data", async (req, res) => {
  try {
    // Separate old and new data based on your criteria
    const oldData = await DataModel.find({
      datetime: { $lt: new Date(datetime) },
    });
    const newData = await DataModel.find({
      datetime: { $gte: new Date(datetime) },
    });

    res.json({ oldData, newData });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});