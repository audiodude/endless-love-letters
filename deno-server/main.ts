// @deno-types="npm:@types/express@4"
import cors from 'npm:cors@2.8';
import express, { request, Request, Response } from 'npm:express@4';
import lunr from 'npm:lunr@2.3';

const app = express();
app.use(cors());
const port = Number(Deno.env.get('PORT')) || 3000;

/**
 * The file `search_documents.jsonl` must be generated first
 * by running the following in the python-server directory before running this script:
 *
 * $ pipenv run python
 * Python 3.12.0 (main, Oct  3 2023, 17:47:52) [GCC 12.3.0] on linux
 * Type "help", "copyright", "credits" or "license" for more information.
 * >>> import documents
 * >>> documents.create_search_output()
 * >>>
 */

const database: { [key: string]: string } = {};

const text = await Deno.readTextFile('search_documents.jsonl');
const documents = text.split('\n').map((line) => {
  const doc = JSON.parse(line);
  database[doc.id] = doc;
  return doc;
});

const idx: lunr.Index = lunr(function (this: lunr.Index) {
  this.ref('id');
  this.field('letter');
  this.metadataWhitelist = ['position'];

  documents.forEach(function (this: lunr.Index, doc) {
    this.add(doc);
  }, this);
});

app.get('/search', (req: Request, res: Response) => {
  const q = req.query?.q;
  if (!q) {
    res.status(400).send('Missing query parameter');
    return;
  }
  console.log(`Searching for: ${q}`);
  res.json(idx.search(q));
});

app.listen(port, () => {
  console.log(`Listening on ${port} ...`);
});
