const https = require('https');
const fs = require('fs');
const path = require('path');

// .env を手動パース (dotenvがない場合のため)
const envPath = path.join(__dirname, '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const RAKUTEN_APP_ID = envContent.match(/RAKUTEN_APP_ID=([^\r\n]+)/)[1];

const keyword = "パナソニック 炊飯器 ビストロ";
const url = `https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&keyword=${encodeURIComponent(keyword)}&applicationId=${RAKUTEN_APP_ID}&hits=1`;

console.log("Fetching URL:", url);

https.get(url, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
        const json = JSON.parse(data);
        if (json.Items && json.Items.length > 0) {
            console.log("Success! Found:", json.Items[0].Item.itemName);
        } else {
            console.log("Failed. No items found. Error:", JSON.stringify(json));
        }
    });
}).on("error", (err) => {
    console.log("Error: " + err.message);
});
