import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:royal_smoke/core/l10n/app_locale.dart';
import 'package:royal_smoke/l10n/app_localizations.dart';

import '../../../core/constants/app_sizes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../features/content/presentation/app_content_provider.dart';
import '../../../shared/widgets/rs_button.dart';
import '../../../shared/widgets/rs_chrome.dart';
import '../../../shared/widgets/rs_fields.dart';
import '../../../shared/widgets/rs_insets.dart';

class VisitScreen extends ConsumerStatefulWidget {
  const VisitScreen({super.key});

  @override
  ConsumerState<VisitScreen> createState() => _VisitScreenState();
}

class _VisitScreenState extends ConsumerState<VisitScreen> {
  final _name = TextEditingController();
  final _phone = TextEditingController();
  final _when = TextEditingController();
  final _comment = TextEditingController();
  bool _tried = false;
  bool _sent = false;

  @override
  void dispose() {
    _name.dispose();
    _phone.dispose();
    _when.dispose();
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
    final l10n = AppLocalizations.of(context);
    final visit = watchContent(ref).screen('visit');
    if (_sent) {
      return RsSafeBody(
        child: Padding(
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
                textOr(visit.successTitle, l10n.visitSuccessTitle),
                textAlign: TextAlign.center,
                style: AppTextStyles.title.copyWith(
                  fontSize: 22,
                  letterSpacing: 22 * 0.2,
                ),
              ),
              const SizedBox(height: AppSizes.s16),
              Text(
                textOr(visit.successBody, l10n.visitSuccessBody),
                textAlign: TextAlign.center,
                style: AppTextStyles.body.copyWith(color: AppColors.textMuted),
              ),
              TextButton(
                onPressed: () => setState(() => _sent = false),
                child: Text(
                  textOr(visit.bodySecondary, l10n.visitNewRequest),
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
        ),
      );
    }

    final nameError = _tried && _name.text.trim().isEmpty;
    final phoneError = _tried && _phone.text.trim().isEmpty;

    return RsSafeBody(
      child: ListView(
        padding: const EdgeInsets.fromLTRB(
          AppSizes.padX,
          24,
          AppSizes.padX,
          AppSizes.s24,
        ),
        children: [
          RsPageHeading(
            kicker: textOr(visit.kicker, l10n.visitKicker),
            title: textOr(visit.title, l10n.visitTitle),
          ),
          const SizedBox(height: 20),
          RsTextField(
            label: l10n.visitNameLabel,
            hint: l10n.visitNameHint,
            controller: _name,
            errorText: nameError ? l10n.visitNamePhoneError : null,
            onChanged: (_) => setState(() {}),
          ),
          const SizedBox(height: 20),
          RsTextField(
            label: l10n.phoneLabel,
            hint: l10n.phonePrefix,
            controller: _phone,
            keyboardType: TextInputType.phone,
            errorText: phoneError && !nameError
                ? l10n.visitNamePhoneError
                : null,
            onChanged: (_) => setState(() {}),
          ),
          const SizedBox(height: 20),
          RsTextField(
            label: l10n.dateLabel,
            hint: l10n.dateHint,
            controller: _when,
            onChanged: (_) => setState(() {}),
          ),
          const SizedBox(height: 20),
          RsTextField(
            label: l10n.commentLabel,
            hint: l10n.commentHint,
            controller: _comment,
            maxLines: 3,
          ),
          const SizedBox(height: AppSizes.s24),
          RsButton(
            label: textOr(visit.ctaPrimary, l10n.visitSendRequest),
            expand: true,
            onPressed: _submit,
          ),
        ],
      ),
    );
  }
}
