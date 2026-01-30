from sqlalchemy.orm import Session
from sqlalchemy import func

from src.app.modules.apurations.models import Apuration
from src.app.modules.guides.models import Guide


def get_dashboard_summary(db: Session, company_id: int):
    # Total de apurações
    total_apurations = (
        db.query(Apuration)
        .filter(Apuration.company_id == company_id)
        .count()
    )

    # Totais de guias
    total_guides = (
        db.query(Guide)
        .join(Apuration)
        .filter(Apuration.company_id == company_id)
        .count()
    )

    guides_paid = (
        db.query(Guide)
        .join(Apuration)
        .filter(
            Apuration.company_id == company_id,
            Guide.status == "PAID",
        )
        .count()
    )

    guides_pending = total_guides - guides_paid

    # Valores
    total_paid = (
        db.query(func.coalesce(func.sum(Guide.amount), 0))
        .join(Apuration)
        .filter(
            Apuration.company_id == company_id,
            Guide.status == "PAID",
        )
        .scalar()
    )

    total_pending = (
        db.query(func.coalesce(func.sum(Guide.amount), 0))
        .join(Apuration)
        .filter(
            Apuration.company_id == company_id,
            Guide.status != "PAID",
        )
        .scalar()
    )

    return {
        "total_apurations": total_apurations,
        "total_guides": total_guides,
        "guides_paid": guides_paid,
        "guides_pending": guides_pending,
        "total_paid": float(total_paid),
        "total_pending": float(total_pending),
    }

def get_dashboard_by_competence(
    db,
    company_id: int,
    competence: str,
):
    query = (
        db.query(Guide)
        .join(Apuration)
        .filter(
            Apuration.company_id == company_id,
            Apuration.competence == competence,
        )
    )

    total_guides = query.count()

    guides_paid = query.filter(Guide.status == "PAID").count()
    guides_pending = total_guides - guides_paid

    total_amount = (
        query.with_entities(func.coalesce(func.sum(Guide.amount), 0))
        .scalar()
    )

    total_paid = (
        query.filter(Guide.status == "PAID")
        .with_entities(func.coalesce(func.sum(Guide.amount), 0))
        .scalar()
    )

    total_pending = total_amount - total_paid

    return {
        "competence": competence,
        "total_guides": total_guides,
        "guides_paid": guides_paid,
        "guides_pending": guides_pending,
        "total_amount": float(total_amount),
        "total_paid": float(total_paid),
        "total_pending": float(total_pending),
    }
    
def get_dashboard_by_tax_type(
    db,
    company_id: int,
):
    rows = (
        db.query(
            Guide.guide_type.label("tax_type"),
            func.count(Guide.id).label("total_guides"),
            func.sum(
                func.case(
                    (Guide.status == "PAID", 1),
                    else_=0,
                )
            ).label("guides_paid"),
            func.coalesce(func.sum(Guide.amount), 0).label("total_amount"),
            func.coalesce(
                func.sum(
                    func.case(
                        (Guide.status == "PAID", Guide.amount),
                        else_=0,
                    )
                ),
                0,
            ).label("total_paid"),
        )
        .join(Apuration)
        .filter(Apuration.company_id == company_id)
        .group_by(Guide.guide_type)
        .all()
    )

    result = []

    for row in rows:
        guides_pending = row.total_guides - row.guides_paid
        total_pending = float(row.total_amount) - float(row.total_paid)

        result.append(
            {
                "tax_type": row.tax_type,
                "total_guides": row.total_guides,
                "guides_paid": row.guides_paid,
                "guides_pending": guides_pending,
                "total_amount": float(row.total_amount),
                "total_paid": float(row.total_paid),
                "total_pending": total_pending,
            }
        )

    return result    