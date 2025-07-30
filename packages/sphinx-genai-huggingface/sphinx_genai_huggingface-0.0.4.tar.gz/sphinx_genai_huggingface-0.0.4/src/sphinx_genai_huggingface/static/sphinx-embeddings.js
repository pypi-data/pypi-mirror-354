// import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.2';
// 
// console.log('v3');
// 
// async function generateEmbedding(text) {
//   // Create a feature-extraction pipeline
//   const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
//   // Compute sentence embeddings
//   const output = await extractor([text], { pooling: 'mean', normalize: true });
//   return output.tolist()[0];
// }
// 
// // async function generateEmbedding(text) {
// //   // Create a feature extraction pipeline
// //   const extractor = await pipeline('feature-extraction', 'nomic-ai/nomic-embed-text-v1', {
// //       quantized: false, // Comment out this line to use the quantized version
// //   });
// //   // Compute sentence embeddings
// //   const texts = ['search_query: Who is Laurens van der Maaten?'];
// //   const embeddings = await extractor(texts, { pooling: 'mean', normalize: true });
// //   console.log(embeddings['data'].length)
// // }
// 
// // https://huggingface.co/nomic-ai/nomic-embed-text-v1
// // https://huggingface.co/models?pipeline_tag=sentence-similarity&library=transformers.js&sort=downloads
// // can maybe compute dot product from transformers.js?
// // https://huggingface.co/Snowflake/snowflake-arctic-embed-xs#using-transformersjs
// 
// // another candidate
// // https://huggingface.co/OrcaDB/gte-base-en-v1.5
// 
// function contentRoot() {
//   return document.documentElement.dataset.content_root;
// }
// 
// async function getEmbeddings() {
//   const response = await fetch(`${contentRoot()}/embeddings.json`);
//   const json = await response.json();
//   return json;
// }
// 
// function override() {
//   Search._performSearch = async (query, searchTerms, excludedTerms, highlightTerms, objectTerms) => {
//     console.log('Hello from custom search!!');
//     const embeddings = await getEmbeddings();
//     const queryEmbedding = await generateEmbedding(query);
//     console.log({query, queryEmbedding, embeddings});
//     const results = embeddings.map(e => [e['docname'], e['title'], e['id'], null, Math.random() * 100, null, 'text']);
//     // https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/static/searchtools.js#L62
//     // return an array called results where each item is an array like this:
//     // [docName, title, anchor, descr, score, _filename, kind]
//     return results;
//   };
// }
// 
// (async () => {
//   document.addEventListener('DOMContentLoaded', (event) => {
//     console.log('DOMContentLoaded');
//     if (typeof Search === 'undefined') {
//       console.log('404');
//       return;
//     }
//     console.log('200');
//     override();
//     // TODO: You might need to destroy the old search results container...
//     const params = new URLSearchParams(window.location.search);
//     if (params.has('q')) {
//       Search.performSearch(params.get('q'));
//     }
//   });
//   await getEmbeddings();
//   await generateEmbedding('Hello, world!');
// })();
