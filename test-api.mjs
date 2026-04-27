import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

const RAKUTEN_APP_ID = process.env.RAKUTEN_APP_ID;

async function test() {
    const keyword = "パナソニック 炊飯器 ビストロ";
    const url = `https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&keyword=${encodeURIComponent(keyword)}&applicationId=${RAKUTEN_APP_ID}&hits=1`;
    
    console.log("Fetching URL:", url);
    const res = await fetch(url);
    const data = await res.json();
    
    if (data.Items && data.Items.length > 0) {
        console.log("Success! Found:", data.Items[0].Item.itemName);
    } else {
        console.log("Failed. No items found. Error:", JSON.stringify(data));
    }
}

test();
