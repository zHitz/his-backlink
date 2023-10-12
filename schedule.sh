#!/bin/sh

# Đường dẫn tới các tệp Python
step1_script="/his-backlink/step1.py"
step2_script="/his-backlink/step2.py"
step3_script="/his-backlink/step3.py"
step4_script="/his-backlink/step4.py"
step5_script="/his-backlink/step5.py"

# Kiểm tra xem step trước đó đã hoàn thành hay chưa và chạy step tiếp theo
if python3 "$step1_script"; then
    if python3 "$step2_script"; then
        if python3 "$step3_script"; then
            if python3 "$step4_script"; then
                python3 "$step5_script"
            fi
        fi
    fi
fi
