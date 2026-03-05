import { connect } from 'nats';

let nc;

export async function connectNATS(url) {
  nc = await connect({ servers: url });
  console.log('NATS connected');
}

export async function request(subject, payload) {
  if (!nc) {
    throw new Error('NATS not initialized');
  }

  const msg = await nc.request(
    subject,
    Buffer.from(JSON.stringify(payload)),
  );

  return JSON.parse(msg.data.toString());
}

