import express from 'express';
import cors from 'cors';
import path from 'path';
import { MongoClient, ServerApiVersion } from 'mongodb';
 import dotenv from 'dotenv';

//Load environment variables from .env file
 dotenv.config();

//MongoDB URI and client setup
// const uri = process.env.MONGODB_URI;
// const uri = "mongodb+srv://demo1:demo1@unis.f9xuu.mongodb.net/?retryWrites=true&w=majority&appName=UNIS";

const client = new MongoClient(process.env.MONGODB_URI);
console.log("Mongo URI:", process.env.MONGO_URI);
// MongoDB collection setup
const dbName = 'unis'; // Database name
const collectionName = 'unis-nupac'; // Collection name where links will be stored

// Function to connect to the database
async function connectDb() {
  try {
    await client.connect();
    console.log("Connected to MongoDB");
    return client.db(dbName).collection(collectionName);
  } catch (error) {
    console.error("Error connecting to MongoDB:", error);
    throw error;
  }
}

const app = express();
const port = process.env.PORT || 3001;

// Middleware
app.use(express.json());  // Use express's built-in JSON parser
app.use(cors());  // Enable cross-origin requests

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(process.cwd(), 'public')));

// Route to serve the main HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(process.cwd(), 'public', 'index.html'));
});

// Route to handle form submission and save the link to MongoDB
app.post('/saveLink', async (req, res) => {
  const { linkName, linkUrl } = req.body;

  if (!linkName || !linkUrl) {
    return res.status(400).json({ success: false, message: 'Link name and URL are required' });
  }

  try {
    const collection = await connectDb();
    await collection.insertOne({ name: linkName, url: linkUrl });
    res.json({ success: true });
  } catch (error) {
    console.error('Error saving link:', error);
    res.status(500).json({ success: false, message: 'Error saving link' });
  }
});

// Route to get all links from MongoDB
app.get('/links', async (req, res) => {
  try {
    const collection = await connectDb();
    const links = await collection.find().toArray();
    res.json({ success: true, data: links });
  } catch (error) {
    console.error('Error fetching links:', error);
    res.status(500).json({ success: false, message: 'Error fetching links' });
  }
});

// Route to handle removing a link from MongoDB
app.delete('/removeLink', async (req, res) => {
  const { id } = req.body;

  if (!id) {
    return res.status(400).json({ success: false, message: 'ID is required' });
  }

  try {
    const collection = await connectDb();
    const result = await collection.deleteOne({ _id: new MongoClient.ObjectID(id) });

    if (result.deletedCount === 1) {
      res.json({ success: true, message: 'Link removed successfully' });
    } else {
      res.status(400).json({ success: false, message: 'No link found to remove' });
    }
  } catch (error) {
    console.error('Error removing link:', error);
    res.status(500).json({ success: false, message: 'Error removing link' });
  }
});

// Route to clear all links from MongoDB
app.delete('/clearLinks', async (req, res) => {
  try {
    const collection = await connectDb();
    const result = await collection.deleteMany({});

    if (result.deletedCount > 0) {
      res.status(200).json({ success: true, message: 'All links deleted' });
    } else {
      res.status(400).json({ success: false, message: 'No links to clear' });
    }
  } catch (error) {
    console.error('Error clearing links:', error);
    res.status(500).json({ success: false, message: 'Error clearing links' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
