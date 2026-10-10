from pathlib import Path
import re

BASE = Path("stock/models")

files = list(BASE.glob("*.py"))

for path in files:
    if path.name == "__init__.py":
        continue

    content = path.read_text(encoding="utf-8")
    original = content

    # Modèles concernés : on ajoute les champs dans chaque classe Model
    # uniquement si le champ n'existe pas déjà dans la classe.
    classes = list(re.finditer(
        r"^class\s+(\w+)\(models\.Model\):",
        content,
        re.MULTILINE
    ))

    for match in reversed(classes):
        class_name = match.group(1)
        start = match.start()
        class_end = len(content)

        # Chercher la prochaine classe
        next_class = re.search(
            r"^class\s+\w+\(models\.Model\):",
            content[match.end():],
            re.MULTILINE
        )

        if next_class:
            class_end = match.end() + next_class.start()

        class_content = content[start:class_end]

        # Ne pas modifier les modèles qui ne sont pas des modèles métier
        # uniquement si nécessaire plus tard.
        additions = []

        if not re.search(r"^\s+slug\s*=", class_content, re.MULTILINE):
            additions.append(
                '    slug = models.SlugField('
                'max_length=150, unique=True, null=True, blank=True, '
                'verbose_name="Slug")'
            )

        if not re.search(r"^\s+statut\s*=", class_content, re.MULTILINE):
            additions.append(
                '    statut = models.CharField('
                'max_length=20, default="actif", '
                'verbose_name="Statut")'
            )

        if not additions:
            continue

        # Insérer les champs avant class Meta / def __str__ / fin de classe
        insertion_match = re.search(
            r"^    class Meta:|^    def __str__\(",
            class_content,
            re.MULTILINE
        )

        if insertion_match:
            insertion_pos = start + insertion_match.start()
        else:
            # Insérer avant la prochaine classe
            insertion_pos = class_end

        block = "\n" + "\n".join(additions) + "\n"

        content = content[:insertion_pos] + block + content[insertion_pos:]

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"MODIFIE : {path}")
    else:
        print(f"OK      : {path}")

print("\nTerminé.")
