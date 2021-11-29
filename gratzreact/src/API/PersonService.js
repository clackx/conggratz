import axios from "axios";
import { jsonURL } from "../constants";

export default class PersonService {
  static async getAll(bdate, lang, limit, offset) {
    const response = await axios.get(jsonURL, {
      params: { bdate, lang, limit, offset }
    })
    return response;
  }

  static async getWikiInfo(namelink, locale) {
    const url = "https://" + locale +
      ".wikipedia.org/w/api.php?action=query&origin=*&format=json" +
      "&prop=extracts&explaintext=1&exintro=1&titles=" + namelink
    const response = await axios.get(url)
    return response;
  }
}
