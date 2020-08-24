Step running aplikasi
1. Buka folder demo via file explorer, copy folder myproject ( file utama )
2. Buka mysql workbench, drop semua table di skema demo, (nanti akan digenerate ulang di proses migrate)
3. Masuk virtual env via cmd, demo>venv\Scripts\activate
4. Masuk folder demo/myproject, lakukan migrate, python manage.py migrate (tidak perlu makemigrations, karena di folder migration sudah dibuatkan initialnya)
5. Optional: Create superuser, python manage.py createsuperuser
6. Run aplikasi, python manage.py runserver
7. Optional: Insert masal data emiten dan list paragraph. 
bisa dicopas kolom "query insert" ke sql editor di mysql workbench, run+commit


untuk case migrate jika ada gagal bisa dicoba untuk generate ulang file migration dan migrate, 
1. drop semua table di SCHEMA demo via mysql workbench
2. buka myproject/nbapp/migration, delete semua file di folder (biasanya ada file: 0001_initial.py dst)
3. generate ulang file migration dengan command: python manage.py makemigrations
4. lakukan migrations: python manage.py migrate
5. optional: insert data emitten dan news list via sql, sesuai data sample di excel