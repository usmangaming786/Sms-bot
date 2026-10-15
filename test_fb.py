from firebase_manager import FirebaseManager

fb = FirebaseManager('https://berlinxmirrorfinalboss-default-rtdb.firebaseio.com')
print('Connected:', fb.test_connection())
devs = fb.get_online_devices()
print(f'Online count: {len(devs)}')
for d in devs:
    print(f"- {d['id']} | Model: {d['model']} | Batt: {d['battery']} | SIMs: {len(d['sims'])}")
