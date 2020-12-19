import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;

import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

public class Main{

    public static void main(String[] args) {

        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

        long m = System.currentTimeMillis();

        System.out.println("Начинается обнаружение");

        CascadeClassifier faceDetector = new CascadeClassifier("./resources/haarcascade_second_train.xml");
        Mat image = Imgcodecs
                .imread("./resources/1.jpg");

        MatOfRect faceDetections = new MatOfRect();
        faceDetector.detectMultiScale(image, faceDetections);

        System.out.println(String.format("Обнаружено %s лиц", faceDetections.toArray().length));

        for (Rect rect : faceDetections.toArray()) {
            Imgproc.rectangle(image, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
                    new Scalar(0, 255, 0));
        }

        System.out.println("Время работы программы: " + (double) (System.currentTimeMillis() - m));

        String filename = "Detected1.png";
        System.out.println(String.format("Результат %s", filename));
        Imgcodecs.imwrite(filename, image);
    }
}