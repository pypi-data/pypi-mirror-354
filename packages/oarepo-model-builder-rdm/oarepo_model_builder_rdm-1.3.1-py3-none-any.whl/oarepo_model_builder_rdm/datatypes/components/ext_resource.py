from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import (
    AppModelComponent,
    ExtResourceModelComponent,
)


class RDMExtResourceModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ExtResourceModelComponent, AppModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if not datatype.profile == "record":
            return
        ext_resource = datatype.definition["ext-resource"]
        ext_resource["service-kwargs"][
            "pids_service"
        ] = "{{invenio_rdm_records.services.pids.PIDsService}}(service_config, {{invenio_rdm_records.services.pids.PIDManager}})"
        datatype.definition["ext-resource"] = ext_resource
