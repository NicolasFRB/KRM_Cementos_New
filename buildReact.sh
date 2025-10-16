#!/bin/bash


cd krm/static/; 
rm main.react.js;
rm main.react.js.map ;
cd ../..;

cd krm-react;
npm ci;
chmod -R 755 ./krm-react/node_modules/.bin/react-scripts*
npm run build; 
mv build/static/js/main.*.js ../krm/static/main.react.js;
mv build/static/js/main.*.js.map ../krm/static/main.react.js.map;
cd ..;
