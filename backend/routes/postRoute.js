import "dotenv/config"
import express from 'express';
import { request as natsRequest } from '../nats/client.js';
import {finalPort, finalIP} from "../src/server.js"

const router = express.Router();

router.post('/images', async (req, res) => {
  const { query } = req.body;

  if (!query || typeof query !== 'string' || !query.trim()) {
    return res.status(400).json({ error: 'Invalid prompt' });
  }

  let reply;
  try {
    reply = await natsRequest(process.env.NATS_SUBJECT ?? nats_subject, { query });

    const finalreply = reply.map( item =>{
      const safefilename = encodeURIComponent(item.filename);
      return{
        url : `http://${finalIP}:${finalPort}/photos/${safefilename}`,
      };
    });

    res.json(finalreply);

  } catch (err) {
    if (err.code === 'TIMEOUT') {
      return res.status(504).json({ error: 'RAG timeout' });
    }
    return res.status(502).json({ error: 'RAG unavailable' });
  }

});
export default router;
