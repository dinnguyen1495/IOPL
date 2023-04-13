from django.core.validators import RegexValidator


class CommaSeparatedStringValidator(RegexValidator):
    regex = r"^(?:[^,]+)(?:,\s*[^,]+)*$"
    message = "Author(s) input should be a single name or a comma-separated text"


class ISBNValidator(RegexValidator):
    regex = r"^(?:ISBN(?:-1[03])?:?●)?(?=[0-9X]{10}$|(?=(?:[0-9]+[-●]){3})" \
            "[-●0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[-●]){4})[-●0-9]{17}$)" \
            "(?:97[89][-●]?)?[0-9]{1,5}[-●]?[0-9]+[-●]?[0-9]+[-●]?[0-9X]$"
    message = "Wrong format input for \"ISBN\" field"


class YearValidator(RegexValidator):
    regex = r"^(19|20)\d{2}$"
    message = "Wrong format input for \"Year\" field"