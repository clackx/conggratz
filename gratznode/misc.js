const { createHash } = require('node:crypto');

function formatData({ wdEntities, occuObj, peopleObj, flagCntryObj, lang }) {
    const result = [];
    for (const wdeRankPair of wdEntities) {
        const [wdEntity, pageViewRank] = Object.values(wdeRankPair);
        person = peopleObj[wdEntity];
        if (person) {
            const occupation = occuObj[wdEntity]
            const flagCntry = flagCntryObj[wdEntity]
            const data = formatObject({
                wdEntity, pageViewRank,
                occupation, person, flagCntry, lang
            })
            result.push(data)
        }
    }
    return result;
}


function formatObject({ wdEntity, pageViewRank, occupation, person, flagCntry, lang }) {
    if (person)
        return {
            'wde': wdEntity,
            'rank': pageViewRank,
            'photo': getWCThumb(person.photo),
            'links': parseAndNormalize(person.links),
            'descrs': parseAndNormalize(person.descrs, capitalize = true),
            'occupations': getTags(occupation, lang),
            'countries': getFlagsAndCountries(flagCntry)
        }
}


function capitalizeString(textString) {
    if (!textString) return
    return textString.charAt(0).toUpperCase() + textString.slice(1)
    // return textString.split(' ').map(
    //     word => word.charAt(0).toUpperCase() +
    //         word.slice(1).toLowerCase()).join(' ');
}


const latList = ['en', 'es', 'fr', 'de', 'it'];
const kyrList = ['ru', 'be', 'uk', 'kk'];
const hierList = ['zh', 'ja', 'ko'];
const languages = [...latList, ...kyrList, ...hierList];
exports.languages = languages;


function parseAndNormalize(dataString, capitalize = false) {
    const resultDict = {};
    let dict = {};

    try {
        dict = JSON.parse(dataString);
    } catch (err) {
        console.log('! Data parse error', err);
        for (let l of languages) resultDict[l] = '--err!data--';
        return resultDict;
    }

    if (capitalize) for (l of languages) dict[l] = capitalizeString(dict[l]);

    const findDefault = ({ obj, list }) => { for (key of list) if (obj[key]) return obj[key] }

    let latDefault = findDefault({ obj: dict, list: latList });
    let kyrDefault = findDefault({ obj: dict, list: kyrList });
    let hierDefault = findDefault({ obj: dict, list: hierList });

    latDefault = latDefault || kyrDefault || hierDefault || '--nodata--';
    kyrDefault = kyrDefault || latDefault;
    hierDefault = hierDefault || latDefault;

    for (l of latList) resultDict[l] = dict[l] || latDefault;
    for (l of kyrList) resultDict[l] = dict[l] || kyrDefault || latDefault;
    for (l of hierList) resultDict[l] = dict[l] || hierDefault || latDefault;

    return resultDict;
}


function getTags(occus, lang) {

    const emojiList = [];
    const fullTagList = [];
    let tagsString = '';

    for (let o of occus || []) {
        let o_em = getEmojiChars(o.emoji);
        let o_dc = parseAndNormalize(o.descr_cache);

        emojiList.push(o_em);
        fullTagList.push([o.occu_entity, o_dc, o_em]);
        tagsString += `#${o_dc[lang].replace(/-| /g, '_')} ${o_em} `;
    }

    tagsString = tagsString || '--notags--';

    let icon = '⁉️';
    if (emojiList.length) {
        icon = emojiList[0];
        icon = icon.split(' ')[0];
        icon = icon.split('-')[0];
    }

    return { icon, 'tags': tagsString, 'list': fullTagList };
}


function getFlagsAndCountries(flags) {
    const countries = [];
    const svg_flags = [];
    const fc_list = [];

    let emojiFlag = '';
    for (f of flags || []) {

        const flagImage = getWCThumb(f.svg_flag, width = 256, format = 'png');
        svg_flags.push(flagImage);
        countries.push(f.country_name);
        fc_list.push([f.country_name, flagImage]);

        if (!emojiFlag)
            emojiFlag = f.emoji_flag;
        if (emojiFlag[0] != 'U' && f.emoji_flag[0] == 'U')
            emojiFlag = f.emoji_flag;
    }

    return { 'icon': getFlagEmoji(emojiFlag), fc_list, svg_flags, countries };
}


function getFlagEmoji(emojis) {
    if (emojis[0] == '-') return getEmojiChars('U+1F5FA');
    if (emojis[0] == '~') return getEmojiChars(emojis.slice(2)) + '*';
    return getEmojiChars(emojis);
}


function getEmojiChars(emojis) {
    if (!emojis) return String.fromCodePoint(128100);
    return emojis.split(' ').map(
        e => String.fromCodePoint('0x' + e.slice(2))).join('');
}


function getWCThumb(imgName, width = 420, format = 'jpg') {
    if (!imgName)
        return `https://conggratz.ru/stati/nophoto${~~(Math.random() * 3) + 1}.jpg`;
    imgName = imgName.replaceAll(' ', '_');
    const d = hashText(imgName);
    let result = 'https://upload.wikimedia.org/wikipedia/commons/thumb/' +
        `${d.slice(0, 1)}/${d.slice(0, 2)}/${imgName}/${width}px-${imgName}`;
    result = result.replaceAll('"', '%22');
    if (result.slice(-3) != format) result += '.' + format;
    return result;
}


function hashText(content, algo = 'md5') {
    const hashFunc = createHash(algo);
    hashFunc.update(content);
    return hashFunc.digest('hex');
}


exports.formatData = formatData;
exports.formatObject = formatObject;
