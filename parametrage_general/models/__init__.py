from .general import (
    TimeStampedModel,
    StatusModel,
    SlugModel,
    Societe,
    Ville,
    Site,
    Direction,
    Departement,
    Service,
    Fonction,
    Specialite,
    UniteMedicale,
    EmailSettings,
    ConfigurationEtablissement,
)

from .actes import (
    CategorieActe,
    ActeMedical,
    TarifActe,
)

from .consultations import (
    TypeConsultation,
    TarifConsultation,
    MotifConsultation,
    Posologie,
    VoieAdministration,
    Dosage,
    Forme,
)

from .examens import (
    CategorieExamen,
    TypeExamen,
    Examen,
    TarifExamen,
)

from .hospitalisation import (
    TypeSejour,
    TypeChambre,
    Chambre,
    Lit,
    TypeSoin,
    RegimeAlimentaire,
    MotifHospitalisation,
    TypeSortie,
    TarifSejour,
)

