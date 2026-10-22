# 📋 ĐÁNH GIÁ TIẾN ĐỘ DỰ ÁN, GIAO BTVN & GIÁO ÁN BUỔI 9 / 10 (120 PHÚT)
## KHÓA HỌC DỰ ÁN LẬP TRÌNH PYTHON CHUYÊN SÂU

---

## PART 1: ĐỌC & ĐÁNH GIÁ CHI TIẾT 4 DỰ ÁN TẠI LỚP

### 1. Dự án: TÙNG LÂM – [TungLam/](file:///c:/Users/ACER/OneDrive%20-%20Thang%20Long%20University/Desktop/Bu%E1%BB%95i%209-20261003T020227Z-1-001/Bu%E1%BB%95i%209/TungLam)
* **Tên sản phẩm:** `Lotus Tactical FPS` (Game bắn súng chiến thuật góc nhìn thứ nhất mô phỏng Valorant bằng Pygame).
* **Điểm mạnh xuất sắc:**
  * Xây dựng thành công kỹ thuật render giả lập không gian 3D (Raycasting engine), camera xoay chuột mượt mà (`update_mouse`).
  * Cơ chế chiến thuật Valorant chuẩn chỉnh:
    * Vũ khí chia hệ số sát thương: `Classic` (thân 26, đầu 78) và `Vandal` (thân 40, đầu 160).
    * Cơ chế Ngồi (`Crouch`): camera hạ thấp 55px, súng hạ xuống tự nhiên bằng nội suy `lerp`.
    * Cơ chế Spike: Cầm Spike, đặt Spike tại 3 Site (A, B, C) với đếm ngược 35s.
    * Giai đoạn chuẩn bị (Buy Phase), tiền thưởng theo round, HUD máu/đạn và Minimap.
* **Tồn tại cần khắc phục:**
  * File `sound.py` đã viết sẵn hàm `play()` nhưng **chưa được gọi** trong `main.py` khi nổ súng, nạp đạn, đặt spike hay thông báo thắng/thua.
  * Bot kẻ địch (`Enemy`) chưa có logic chạy lại gỡ Spike (`Defuse`) khi người chơi đã đặt bom thành công.
  * Mua súng mới chỉ gán phím tắt số `1`, chưa có giao diện Shop Buy Phase trực quan.

---

### 2. Dự án: NHÓM CYBER ESCAPE – [cyberesc/](file:///c:/Users/ACER/OneDrive%20-%20Thang%20Long%20University/Desktop/Bu%E1%BB%95i%209-20261003T020227Z-1-001/Bu%E1%BB%95i%209/cyberesc)
* **Tên sản phẩm:** `Cyber Escape` (Game 2D Platformer / Cyberpunk Shooter).
* **Điểm mạnh xuất sắc:**
  * **Cấu trúc kiến trúc code OOP rất chuyên nghiệp:** Tách biệt rõ ràng `GameEngine`, `game_engine_gameplay.py`, `game_engine_layout.py`.
  * Vẽ mô hình súng Pixel Art trực tiếp bằng mã nguồn (mảng ký tự màu trong `weapon.py`), không phụ thuộc ảnh ngoài.
  * Hoàn thành hệ thống **8 Màn chơi (`levels/lv1.py` đến `lv8.py`)** với đa dạng kẻ địch: quái cận chiến, quái bay (`FlyingEnemy`) và Đại Boss cuối 1500 HP.
  * Có hệ thống nâng cấp chỉ số nhân vật (HP, Damage, Speed) và nhặt PowerUps trên map.
* **Tồn tại cần khắc phục:**
  * Chưa có module lưu dữ liệu (Save Game): tắt game là mất hết Coins và cấp độ mở khóa `max_unlocked_level`.
  * Boss màn 8 lượng máu rất trâu (1500 HP) nhưng thiếu cơ chế cuồng nộ (Rage Phase) khi máu thấp.
  * Khi người chơi bắn cạn băng đạn (`AMMO`) dễ bị kẹt nếu không tìm thấy hòm đạn tiếp tế.

---

### 3. Dự án: FOOTBALL MANAGER WEB – [football_manager_web/](file:///c:/Users/ACER/OneDrive%20-%20Thang%20Long%20University/Desktop/Bu%E1%BB%95i%209-20261003T020227Z-1-001/Bu%E1%BB%95i%209/football_manager_web)
* **Tên sản phẩm:** `Football Manager Web` (Game Quản lý CLB Bóng đá - Flask, SQLite & Dynamic Web UI).
* **Điểm mạnh xuất sắc:**
  * Dự án có quy mô đồ sộ bậc nhất: hơn 2600 dòng code Python backend (`app.py`), database SQLite hoàn chỉnh (`Club`, `Player`, `Coach`, `MatchHistory`, `LeagueStanding`, `YouthPlayer`).
  * Hệ thống tính năng sâu: Chọn đội hình 11 người (`select_xi`), Mô phỏng trận đấu trực tiếp theo phút (`live_match`), Chuyển nhượng (`transfer_market`), Học viện trẻ (`youth_academy`), Phòng cúp (`trophy_room`).
  * Tích hợp Widget nghe nhạc FIFA Soundtrack tự động nhúng vào mọi trang cực kỳ ấn tượng.
* **Tồn tại & Đã xử lý:**
  * Đã giải nén phục hồi 16 file giao diện `.html` trong `templates/` (trước đó chỉ có file `.docx` khiến Flask không render được giao diện).
  * Cần hoàn thiện cơ chế thể lực (`stamina`) và chấn thương/thẻ phạt sau trận để người chơi có động lực dùng tính năng thay người (`substitute`).

---

### 4. Dự án: BLADE MASTER 2D – [P.PY_merged.py](file:///c:/Users/ACER/OneDrive%20-%20Thang%20Long%20University/Desktop/Bu%E1%BB%95i%209-20261003T020227Z-1-001/Bu%E1%BB%95i%209/P.PY_merged.py)
* **Tên sản phẩm:** `Blade Master 2D` (Game đối kháng kiếm sĩ 2D góc nhìn ngang - 2D Side-view Sword Fighting bằng Pygame).
* **Điểm mạnh xuất sắc:**
  * **Hệ thống cơ chế chiến đấu (Combat Mechanics) cực kỳ có chiều sâu:**
    * **Hệ thống Thế kiếm (Stances):** 3 thế `HIGH` (Đánh mạnh), `MID` (Cân bằng), `LOW` (Thủ giảm 20% sát thương nhận) chuyển đổi linh hoạt bằng phím `1`, `2`, `3`.
    * **Đa dạng đòn đánh:** Đòn nhẹ `E` (hồi chiêu nhanh, tốn ít stamina), Đòn nặng `Y` (sát thương lớn), Tuyệt kỹ Skill `C` (tầm quét rộng 160px, chém hiệu ứng ánh sáng tím), Đòn phản công Counter `V` (chỉ kích hoạt khi đối thủ bị choáng).
    * **Cơ chế phòng thủ chuẩn game Souls-like:** Đỡ đòn hoàn hảo (`Parry` phím `Z`) làm đối phương choáng 1.4s; Lướt né đòn (`Dodge` phím `X`) làm đối phương choáng 0.8s.
  * **AI Bot Ryu thông minh:** Biết tự đổi thế kiếm khắc chế người chơi, tự tính toán khoảng cách áp sát, tự né đòn/parry theo xác suất và tự tung combo skill.
  * **Hệ thống Chợ rèn (Shop):** Nâng cấp Kiếm tăng sát thương đòn đánh, nâng cấp Giáp tăng % giảm sát thương, cơ chế thưởng/phạt vàng sau trận đấu (`+2000` / `-1000` vàng).
  * **Đồ họa tự sinh bằng code (Procedural Art) & Game Feel:** Vẽ mặt trăng, tòa nhà thành phố đêm, hiệu ứng hạt nổ văng ra khi trúng đòn (`Particle`), nhấp nháy trắng khi dính sát thương (`hit_flash`).
* **Tồn tại cần khắc phục:**
  * **Cấu trúc file dồn cục:** Gần 2000 dòng code nằm chung trong 1 file duy nhất (`P.PY_merged.py`), chưa module hóa (cần tách `fighter.py`, `ai.py`, `shop.py`, `config.py`).
  * **Hiệu ứng Rung màn hình (`screen_shake`) chưa hoạt động:** Trong code có gán `self.screen_shake = 0.12` khi trúng đòn, nhưng trong toàn bộ hàm `render()` và `draw_fighter()` lại **chưa hề áp dụng offset rung vào tọa độ vẽ camera/surface**.
  * **Âm thanh:** Đã định nghĩa hàm `play_sound` và từ điển `SOUND_FILES` nhưng chưa có sẵn thư mục `sounds/` chứa file âm thanh thật nên hiện tại game đang ở chế độ câm.
  * **Cân bằng Game (Balancing):** Vàng khởi đầu cho quá lớn (`START_GOLD = 10000`), nâng cấp vài lần là max đồ ngay từ đầu; chưa có thời gian trễ hồi thể lực (`stamina delay`) nên người chơi dễ spam né liên tục.

---

## 📝 PART 2: BỘ BÀI TẬP VỀ NHÀ (BTVN) CHO TỪNG BẠN

### 🎯 1. BTVN CHO TÙNG LÂM (`TungLam`)
1. **Mức Cơ bản (Tích hợp âm thanh):**
   * Import hàm `play` từ `sound.py` vào `main.py`.
   * Kích hoạt âm thanh tương ứng tại: `player_shoot()`, `start_reload()`, `win_round()`, `lose_round()`.
2. **Mức Khá (Bot biết gỡ Spike):**
   * Khi `spike_planted == True`, nếu bot còn sống và lại gần tọa độ Spike trong bán kính 60px, bot bắt đầu giữ vị trí gỡ bom (7 giây). Nếu quá 7 giây không bị tiêu diệt $\to$ Bot gỡ thành công $\to$ Gọi `lose_round()`.
3. **Mức Thử thách:** Bổ sung khẩu súng ngắm `OPERATOR` (Giá: 4700$, 1 viên nạp lại, bắn trúng là hạ gục ngay).

---

### 🎯 2. BTVN CHO NHÓM CYBER ESCAPE (`cyberesc`)
1. **Mức Cơ bản (Lưu dữ liệu Save Game):**
   * Tạo file `save_manager.py` dùng module `json` để lưu và tải: `coins`, `max_unlocked_level`, `hp_lvl`, `dmg_lvl`.
   * Tự động lưu khi qua màn và nạp lại khi mở game.
2. **Mức Khá (Hồi đạn tự động / Đánh cận chiến):**
   * Khi `ammo == 0`, nếu người chơi bấm bắn thì tung ra đòn cận chiến đánh gần (hoặc khẩu súng mặc định tự hồi 1 viên sau mỗi 1.5 giây).
3. **Mức Thử thách (Boss Rage Phase màn 8):**
   * Khi Boss còn dưới 30% HP (< 450 HP): Boss đổi tông màu sang đỏ rực, tốc độ xả đạn nhanh gấp đôi và triệu hồi 2 con `FlyingEnemy`.

---

### 🎯 3. BTVN CHO FOOTBALL MANAGER WEB (`football_manager_web`)
1. **Mức Cơ bản (Kiểm tra hệ thống):**
   * Khởi động server `python app.py`, duyệt qua các trang Dashboard, Squad, Live Match, Transfer để đảm bảo toàn bộ HTML hoạt động mượt mà.
2. **Mức Khá (Cơ chế tiêu hao thể lực):**
   * Sau mỗi trận đấu mô phỏng, trừ 5 - 10 điểm `stamina` của 11 cầu thủ đá chính.
   * Cầu thủ có `stamina < 50` sẽ bị giảm 20% chỉ số tấn công và phòng ngự trong trận kế tiếp.
3. **Mức Thử thách (Bảng tin tức CLB):**
   * Tạo bảng thông báo tin tức tại `dashboard.html` hiển thị các sự kiện: ký hợp đồng, thưởng tiền nhà tài trợ, kết quả trận đấu vừa đá.

---

### 🎯 4. BTVN CHO BLADE MASTER 2D (`P.PY_merged.py`)
1. **Mức Cơ bản (Kích hoạt Screen Shake & Cân bằng Vàng):**
   * Hiện thực hóa `self.screen_shake`: Khi `self.screen_shake > 0`, tạo ngẫu nhiên `offset_x = random.randint(-5, 5)` và `offset_y = random.randint(-5, 5)`, áp dụng render toàn bộ frame lên một Surface đệm và blit lệch tọa độ lên màn hình chính.
   * Chỉnh lại `START_GOLD = 500` và giá nâng cấp tăng dần theo cấp độ (`cấp * 1000 vàng`).
2. **Mức Khá (Cơ chế Hồi Stamina chuẩn xác):**
   * Thêm biến `stamina_cooldown`: Khi vừa đánh hoặc lướt né/parry, stamina bị ngừng hồi trong 0.8 giây, sau đó mới hồi dần 25 điểm/giây để tránh spam né liên tục.
   * Thêm âm thanh chém kiếm và va chạm thực tế vào thư mục `sounds/`.
3. **Mức Thử thách (Boss Ryu Cuồng nộ - Phase 2):**
   * Khi Boss Ryu còn dưới 35% máu (< 350 HP): Kích hoạt Phase 2, hào quang đỏ rực quanh người, tốc độ lướt tăng gấp đôi và mở khóa chiêu "Bão Kiếm" chém liên tiếp 3 đòn.

---

## ⏱️ PART 3: GIÁO ÁN CHI TIẾT DẠY LỚP TRONG 120 PHÚT
### CHỦ ĐỀ: TỐI ƯU HÓA ENGINE, HOÀN THIỆN TÍNH NĂNG ĐẶC TRƯNG & CHUẨN BỊ DEMO SẢN PHẨM

> **Chiến lược sư phạm:** Lớp học theo mô hình **Project-based Learning (PBL)** với 4 dự án đa dạng. Giáo viên không dạy lý thuyết một chiều suốt buổi mà chia thành **Micro-lecture chung (20 phút)** $\to$ **Sprint thực hành kèm cặp 1-1 (60 phút)** $\to$ **Showcase & Playtest nội bộ (15 phút)**.

| Thời lượng | Giai đoạn | Hoạt động của Giáo viên & Học sinh | Mục tiêu cần đạt |
| :---: | :--- | :--- | :--- |
| **00 – 15'**<br>*(15 phút)* | **Khởi động & Check BTVN** | • Giáo viên tới từng máy kiểm tra tiến độ làm BTVN của 4 dự án.<br>• Cho mỗi bạn chiếu nhanh 1 tính năng mới tự làm ở nhà lên màn hình.<br>• Tuyên dương bạn có nỗ lực tốt, tạo không khí hào hứng đầu giờ. | Nắm bắt ngay tình trạng bài làm ở nhà của từng bạn. |
| **15 – 35'**<br>*(20 phút)* | **Chuyên đề chung: Game Polish & Trải nghiệm người dùng (UX)** | • **Lý thuyết chung (10p):** Khái niệm *Game Feel* & *Juice* (Rung màn hình, hiệu ứng chớp sáng, âm thanh phản hồi, độ mượt khi tương tác).<br>• **Thực hành mẫu trên máy chiếu (10p):**<br>  1. Cách cài đặt thuật toán Rung màn hình (Screen Shake) áp dụng cho cả 3 game Pygame.<br>  2. Cách tạo thông báo Flash Message / Toast động (dùng cho Web Football Manager). | Giúp cả lớp nâng tầm sản phẩm từ "chạy được" sang "chơi cuốn hút, đã mắt". |
| **35 – 95'**<br>*(60 phút)* | **Sprint Nước Rút & Mentor 1-1 theo trạm** | **Giáo viên xoay vòng hỗ trợ chuyên sâu từng dự án (mỗi trạm 12-15 phút):**<br>• **Trạm 1 (Tùng Lâm - Lotus FPS):** Ghép hàm `play()` từ `sound.py` vào `main.py` khi nổ súng & Viết logic bot phát hiện Spike để defuse.<br>• **Trạm 2 (Cyber Escape):** Hướng dẫn viết `save_manager.py` đọc/ghi JSON chuẩn, xử lý ngoại lệ `FileNotFoundError`.<br>• **Trạm 3 (Football Manager Web):** Hướng dẫn công thức suy giảm thể lực sau trận trong `app.py` & Render badge thể lực trên `squad.html`.<br>• **Trạm 4 (Blade Master 2D):** Hướng dẫn nhúng Screen Shake Surface & Cân bằng lại giá trị Stamina / Gold. | Mỗi học sinh tự tay hoàn thành xong ít nhất 1 tính năng lớn mới ngay tại lớp. |
| **95 – 110'**<br>*(15 phút)* | **Showcase & Playtest chéo nội bộ** | • Cho các bạn đổi máy chơi thử sản phẩm của nhau:<br>  * Bạn làm Web sang trải nghiệm thử Lotus FPS và Blade Master.<br>  * Các bạn làm Game thử cầm CLB bóng đá trên Web.<br>• Góp ý chéo nhau về độ khó, độ mượt và lỗi giao diện. | Rèn luyện tư duy phản biện, kỹ năng thuyết trình và tự hào về sản phẩm. |
| **110 – 120'**<br>*(10 phút)* | **Tổng kết & Giao mục tiêu Buổi tiếp theo** | • Tổng kết tiến độ từng dự án trên bảng lớp.<br>• Chốt danh mục tính năng cho phiên bản Beta Release.<br>• Nhắc nhở nộp bài và dặn dò các bạn chuẩn bị slide giới thiệu dự án. | Học sinh nắm rõ đầu việc cụ thể cần làm trong tuần. |

---

## 📢 MẪU TIN NHẮN GỬI NHÓM LỚP / PHỤ HUYNH

```text

```
