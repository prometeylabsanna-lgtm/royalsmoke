import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_fields.dart';

class VisitScreen extends StatefulWidget {
  const VisitScreen({super.key});

  @override
  State<VisitScreen> createState() => _VisitScreenState();
}

class _VisitScreenState extends State<VisitScreen> {
  final _name = TextEditingController();
  final _phone = TextEditingController();
  final _date = TextEditingController();
  final _time = TextEditingController();
  final _comment = TextEditingController();
  bool _tried = false;
  bool _sent = false;

  @override
  void dispose() {
    _name.dispose();
    _phone.dispose();
    _date.dispose();
    _time.dispose();
    _comment.dispose();
    super.dispose();
  }

  void _submit() {
    if (_name.text.trim().isEmpty || _phone.text.trim().isEmpty) {
      setState(() => _tried = true);
      return;
    }
    setState(() {
      _sent = true;
      _tried = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_sent) {
      return Padding(
        padding: const EdgeInsets.all(AppSizes.padX),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 88,
              height: 88,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: AppColors.gold),
              ),
              child: const Icon(Icons.check, color: AppColors.gold, size: 28),
            ),
            const SizedBox(height: 20),
            Text(
              'ЗАПИТ НАДІСЛАНО',
              textAlign: TextAlign.center,
              style: AppTextStyles.title.copyWith(fontSize: 22, letterSpacing: 22 * 0.2),
            ),
            const SizedBox(height: AppSizes.s16),
            Text(
              'Ми звʼяжемося з вами, щоб підтвердити дату та час візиту.',
              textAlign: TextAlign.center,
              style: AppTextStyles.body.copyWith(color: AppColors.textMuted),
            ),
            TextButton(
              onPressed: () => setState(() => _sent = false),
              child: Text(
                'НОВИЙ ЗАПИТ',
                style: TextStyle(
                  fontFamily: AppTextStyles.family,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 12 * 0.24,
                  color: AppColors.seashell,
                ),
              ),
            ),
          ],
        ),
      );
    }

    final nameError = _tried && _name.text.trim().isEmpty;
    final phoneError = _tried && _phone.text.trim().isEmpty;

    return ListView(
      padding: const EdgeInsets.fromLTRB(AppSizes.padX, 8, AppSizes.padX, AppSizes.s24),
      children: [
        RsBackBar(label: 'Дім', onPressed: () => context.go('/house')),
        const RsPageHeading(kicker: 'Дім Royal Smoke', title: 'Візит'),
        const SizedBox(height: 20),
        RsTextField(
          label: 'Імʼя',
          hint: 'Ваше імʼя',
          controller: _name,
          errorText: nameError ? 'Вкажіть імʼя та телефон' : null,
          onChanged: (_) => setState(() {}),
        ),
        const SizedBox(height: 20),
        RsTextField(
          label: 'Телефон',
          hint: '+380',
          controller: _phone,
          keyboardType: TextInputType.phone,
          errorText: phoneError && !nameError ? 'Вкажіть імʼя та телефон' : null,
          onChanged: (_) => setState(() {}),
        ),
        const SizedBox(height: 20),
        Row(
          children: [
            Expanded(child: RsTextField(label: 'Дата', hint: 'ДД.ММ.РРРР', controller: _date)),
            const SizedBox(width: AppSizes.s12),
            Expanded(child: RsTextField(label: 'Час', hint: 'ГГ:ХХ', controller: _time)),
          ],
        ),
        const SizedBox(height: 20),
        RsTextField(label: 'Коментар', hint: 'Необовʼязково', controller: _comment, maxLines: 3),
        const SizedBox(height: AppSizes.s24),
        RsButton(label: 'Надіслати запит', expand: true, onPressed: _submit),
      ],
    );
  }
}
