import org.apache.commons.io.FileUtils;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class FileReader {
    public void download(String token, String id, String format) {
        try {
            String path = "https://api.telegram.org/bot" + token + "/getFile?file_id=" + id;
            JSONObject json = readJsonFromUrl(path);
            String namePath = json.getJSONObject("result").getString("file_path");
            String newURL = "https://api.telegram.org/file/bot" + token + "/" + namePath;
            // чтобы сохранять на диск С нужно запустить IDEA под админом
            FileUtils.copyURLToFile(new URL(newURL), new File("C:\\" + id + format));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String readAll(Reader reader) throws IOException {
        StringBuilder sb = new StringBuilder();
        int cp;
        while ((cp = reader.read()) != -1) {
            sb.append((char) cp);
        }
        return sb.toString();
    }

    public JSONObject readJsonFromUrl(String url) throws IOException, JSONException {
        try (InputStream inputStream = new URL(url).openStream()) {
            BufferedReader br = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
            String jsonText = readAll(br);
            return new JSONObject(jsonText);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
