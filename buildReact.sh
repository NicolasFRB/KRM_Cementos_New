#!/bin/bash


cd krm/static/; 
rm main.react.js;
rm main.react.js.map ;
cd ../..;

cd krm-react;
npm i;
npm run build; 
mv build/static/js/main.*.js ../krm/static/main.react.js;
mv build/static/js/main.*.js.map ../krm/static/main.react.js.map;
cd ..;
