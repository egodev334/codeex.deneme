import argparse
import time

import cv2

from wifi_camera_guard.overlay import status_from_rssi
from wifi_camera_guard.wifi_reader import sample_rssi


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="WiFi sinyal gücünü izleyip kamera görüntüsüne yazan örnek uygulama.",
    )
    parser.add_argument(
        "--iface",
        help="RSSI okumak için WiFi arayüz adı (örn. wlan0). Boşsa simülasyon çalışır.",
        default=None,
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=-70.0,
        help="Engel olasılığı için RSSI eşiği (dBm). Varsayılan: -70.",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="OpenCV kamera indeksi. Varsayılan: 0.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    capture = cv2.VideoCapture(args.camera)
    if not capture.isOpened():
        raise SystemExit("Kamera açılamadı. Kamera indeksini kontrol edin.")

    last_sample = time.time()
    status = status_from_rssi(-100.0, "init", args.threshold)

    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                break

            now = time.time()
            if now - last_sample >= 0.5:
                rssi_sample = sample_rssi(args.iface)
                status = status_from_rssi(
                    rssi_sample.value_dbm,
                    rssi_sample.source,
                    args.threshold,
                )
                last_sample = now

            overlay_color = (0, 0, 255) if status.obstacle_likely else (0, 200, 0)
            cv2.putText(
                frame,
                f"RSSI: {status.rssi_dbm:.1f} dBm ({status.source})",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                "ENGEL OLABILIR" if status.obstacle_likely else "SINYAL NORMAL",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                overlay_color,
                2,
            )
            cv2.imshow("WiFi Camera Guard", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
