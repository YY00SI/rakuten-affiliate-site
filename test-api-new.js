const https = require('https');
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const RAKUTEN_APP_ID = envContent.match(/RAKUTEN_APP_ID=([^\r\n]+)/)[1];
const RAKUTEN_ACCESS_KEY = envContent.match(/RAKUTEN_ACCESS_KEY=([^\r\n]+)/)[1];

const keyword = "パナソニック 炊飯器 ビストロ";
// 新エンドポイント
const url = `https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601?format=json&keyword=${encodeURIComponent(keyword)}&applicationId=${RAKUTEN_APP_ID}&accessKey=${RAKUTEN_ACCESS_KEY}&hits=1`;

console.log("Fetching URL:", url);

const options = {
    headers: {
        'Referer': 'https://github.com',
        'Origin': 'https://github.com'
    }
};

https.get(url, options, (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            if (json.Items && json.Items.length > 0) {
                console.log("Success! Found:", json.Items[0].Item.itemName);
            } else {
                console.log("Failed. No items found. Response:", data);
            }
        } catch (e) {
            console.log("Parse Error:", e.message);
            console.log("Raw Data:", data);
        }
    });
}).on("error", (err) => {
    console.log("Error: " + err.message);
});
