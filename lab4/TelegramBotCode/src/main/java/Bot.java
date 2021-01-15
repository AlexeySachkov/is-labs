import org.telegram.telegrambots.ApiContextInitializer;
import org.telegram.telegrambots.bots.DefaultBotOptions;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.ApiContext;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.AnswerCallbackQuery;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.methods.send.SendPhoto;
import org.telegram.telegrambots.meta.api.objects.Message;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.ReplyKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.exceptions.TelegramApiRequestException;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;


public class Bot extends TelegramLongPollingBot {
    private String imagePath;
    private String stylePath;
    private String fileName;
    private boolean docFlag = false;
    private boolean fileFlag = false;
    private final ArrayList<String> styleList = new ArrayList<>(Arrays.asList("abstract", "la muse", "rain", "shipwreck", "space", "udnie"));


    private enum MessageType {
        TEXT,
        PHOTO
    }

    public Bot(DefaultBotOptions botOptions) {
        super(botOptions);
    }

    public Bot() {
    }

    public static void main(String[] args) {
        ApiContextInitializer.init();
        authorization();
    }

    @Override
    public void onUpdateReceived(Update update) {
        if (update.getMessage() != null) {
            if (update.getMessage().hasText()) {
                if (update.getMessage().getText().equals("/start")) {
                    sendMsg(update.getMessage(), "Привет!");
                }
                if (update.getMessage().getText().equals("/info")) {
                    sendMsg(update.getMessage(), "Информация о боте");
                }
                if (update.getMessage().getText().equals("/help")) {
                    sendMsg(update.getMessage(), "Информация о помощи");
                }
                if (update.getMessage().getText().equals("/styles")) {
                    sendMsg(update.getMessage(), "Стили");
                }
                checkStyle(update);
            }
            if (update.getMessage().hasPhoto() || update.getMessage().hasDocument()) {
                FileReader fileReader = new FileReader();
                docFlag = false;
                fileFlag = false;
                if (update.getMessage().getPhoto() != null || update.getMessage().getDocument() != null) {
                    String id;
                    if (update.getMessage().getPhoto() != null) {
                        fileFlag = true;
                         id = update.getMessage().getPhoto().get(0).getFileId();
                    } else {
                        docFlag = true;
                        id = update.getMessage().getDocument().getFileId();
                    }
                    String format = ".jpg";
                    imagePath = "C:\\" + id + format;
                    fileReader.download(getBotToken(), id, ".jpg");
                    sendMsg(update.getMessage(), "Выберите стиль обработки");
                }
            }
        }

//      ответ на нажатие inlineButton
        if (update.getCallbackQuery() != null) {
            answerCallbackQuery(update.getCallbackQuery().getId(), update.getCallbackQuery().getData());
        }
    }

    /**
     * Метод для отправки сообщений и добавления меню
     */
    public void sendMsg(Message message, String text) {
        SendMessage sendMessage = new SendMessage();
        sendMessage.enableMarkdown(true);
        sendMessage.setChatId(message.getChatId());
        sendMessage.setText(text);
        try {
            if (message.hasText()) {
                if (message.getText().equals("/styles")) {
                    setButton(sendMessage, MessageType.PHOTO);
                } else {
                    setButton(sendMessage, MessageType.TEXT);
                }
            }
            if (message.hasPhoto() || message.hasDocument()) {
                setButton(sendMessage, MessageType.PHOTO);
            }
            if (text.equals("Вам понравилась обработка?")) {
                setInlineButton(sendMessage);
            }
            execute(sendMessage);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Метод ответа на нажатие на элемент Inline-клавиатуры
     */
    public synchronized void answerCallbackQuery(String callbackId, String callbackData) {
        AnswerCallbackQuery answer = new AnswerCallbackQuery();
        answer.setCallbackQueryId(callbackId);
        if (callbackData.equals("Like")) {
            answer.setText("😍😍😍");
        } else {
            answer.setText("😓😓😓");
        }
        answer.setShowAlert(true);
        try {
            execute(answer);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getBotUsername() {
        return "NeuralNetworkNSTUBot";
    }

    @Override
    public String getBotToken() {
        return "1022333017:AAEvgnr28g8nJqlz-JHMpPDg4GHZWNrpocw";
    }

    private boolean addStyleAction(String imagePath, String styleName) {
        switch (styleName) {
            case "abstract": {
                stylePath = "abstract.ckpt";
                fileName = "C:\\result1.jpg";
                break;
            }
            case "la muse": {
                stylePath = "la_muse.ckpt";
                fileName = "C:\\result2.jpg";
                break;
            }
            case "rain": {
                stylePath = "rain_princess.ckpt";
                fileName = "C:\\result3.jpg";
                break;
            }
            case "shipwreck": {
                stylePath = "shipwreck.ckpt";
                fileName = "C:\\result4.jpg";
                break;
            }
            case "space": {
                stylePath = "space.ckpt";
                fileName = "C:\\result5.jpg";
                break;
            }
            case "udnie": {
                stylePath = "udnie.ckpt";
                fileName = "C:\\result6.jpg";
                break;
            }
            default:
                return false;
        }

        imagePath = imagePath.replace("\\", "\\\\");
        String command =
                "cmd /c start python C:\\tensorflow-fast-style-transfer-master/run_test.py --content " + imagePath +
                        " --style_model C:\\\\tensorflow-fast-style-transfer-master\\models/" +
                        stylePath + " --output " + fileName;
        try {
            Process pythonProcess = Runtime.getRuntime().exec(command);
            pythonProcess.waitFor();
            pythonProcess.destroy();
        } catch (IOException | InterruptedException e) {
            Logger.getAnonymousLogger().log(Level.SEVERE, "Ошибка при обработке фото");
        }
        return true;
    }

    private void sendPhoto(Update update) {
        SendPhoto sendPhoto = new SendPhoto().setPhoto(new File(fileName));
        sendPhoto.setChatId(update.getMessage().getChatId());
        try {
            execute(sendPhoto);
            sendMsg(update.getMessage(), "Вам понравилась обработка?");
        } catch (TelegramApiException e) {
            sendMsg(update.getMessage(), "Не удалось обработать фото :(\nПопробуйте еще раз...");
            Logger.getAnonymousLogger().log(Level.SEVERE, "Ошибка при отправке фото");
        }
    }

    /**
     * Метод добавления кнопок в ответ на текстовое сообщение
     */
    private void setButton(SendMessage message, MessageType type) {
        ReplyKeyboardMarkup keyboard = new ReplyKeyboardMarkup();
        message.setReplyMarkup(keyboard);
        keyboard.setResizeKeyboard(true);
        keyboard.setSelective(true);
        keyboard.setOneTimeKeyboard(false);

        ArrayList<KeyboardRow> keyboardRowList = new ArrayList<>();
        KeyboardRow keyboardRow1 = new KeyboardRow();
        KeyboardRow keyboardRow2 = new KeyboardRow();

        switch (type) {
            case TEXT:
                keyboardRow1.add(new KeyboardButton("/info"));
                keyboardRow1.add(new KeyboardButton("/help"));
                keyboardRow1.add(new KeyboardButton("/styles"));
                keyboardRowList.add(keyboardRow1);
                break;
            case PHOTO:
                keyboardRow1.add(new KeyboardButton("abstract"));
                keyboardRow1.add(new KeyboardButton("la muse"));
                keyboardRow1.add(new KeyboardButton("rain"));
                keyboardRow2.add(new KeyboardButton("shipwreck"));
                keyboardRow2.add(new KeyboardButton("space"));
                keyboardRow2.add(new KeyboardButton("udnie"));
                keyboardRowList.add(keyboardRow1);
                keyboardRowList.add(keyboardRow2);
                break;
            default:
                Logger.getAnonymousLogger().log(Level.SEVERE, "Неизвестный тип сообщения " + type);
                break;
        }
        keyboard.setKeyboard(keyboardRowList);
    }

    /**
     * Метод для установки Inline-клавиатуры
     */
    private void setInlineButton(SendMessage message) {
        if (message != null) {
            ArrayList<List<InlineKeyboardButton>> buttons = new ArrayList();
            ArrayList<InlineKeyboardButton> buttons1 = new ArrayList();
            buttons1.add(new InlineKeyboardButton().setText("👍").setCallbackData("Like"));
            buttons1.add(new InlineKeyboardButton().setText("👎").setCallbackData("Dislike"));

            buttons.add(buttons1);

            InlineKeyboardMarkup markupKeyboard = new InlineKeyboardMarkup();
            markupKeyboard.setKeyboard(buttons);
            message.setReplyMarkup(markupKeyboard);
        }
    }

    private static void authorization() {
        TelegramBotsApi telegramBotsApi = new TelegramBotsApi();
        //useProxy(telegramBotsApi);
        try {
            telegramBotsApi.registerBot(new Bot());
        } catch (TelegramApiRequestException e) {
            Logger.getAnonymousLogger().log(Level.SEVERE, "Ошибка авторизации с впн" + e);
        }
    }

    private static void useProxy(TelegramBotsApi telegramBotsApi) {
        DefaultBotOptions botOptions = ApiContext.getInstance(DefaultBotOptions.class);
        botOptions.setProxyHost("162.243.32.120");
        botOptions.setProxyPort(61237);
        botOptions.setProxyType(DefaultBotOptions.ProxyType.SOCKS5);

        try {
            telegramBotsApi.registerBot(new Bot(botOptions));
        } catch (TelegramApiRequestException e) {
            Logger.getAnonymousLogger().log(Level.SEVERE, "Ошибка авторизации с прокси " + e);
        }
    }

    private void checkStyle(Update update) {
        String styleName = update.getMessage().getText();
        if (styleList.contains(styleName)) {
            if (imagePath != null) {
                sendMsg(update.getMessage(), "Ваше фото обрабатывается\nПожалуйста подождите...");
                if (addStyleAction(imagePath, styleName)) {
                    try {
                        if (fileFlag) {
                            Thread.sleep(7000);
                        } else {
                            Thread.sleep(15000);
                        }
                        sendPhoto(update);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                } else {
                    sendMsg(update.getMessage(), "Указан неверный стиль");
                }
            } else {
                sendMsg(update.getMessage(), "Пожалуйста, отправте мне фото и выберите стиль еще раз");
            }
        }
    }
}