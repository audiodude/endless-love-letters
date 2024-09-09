// @deno-types="npm:@types/express@4"
import express, { Request, Response } from 'npm:express@4.19.2';

const app = express();
const port = Number(Deno.env.get('PORT')) || 3000;

app.get('/', (_req: Request, res: Response) => {
  res.status(200).send('Hello from Deno and Express!');
});

app.listen(port, () => {
  console.log(`Listening on ${port} ...`);
});
