{
    "resourceType":"Encounter",

    "identifier":[
            {
            "value":"22429197",    //B:hadm_id (admissions)
           }],

            "class":{
                    "code":"EW EMER."},   //F:admission_type(admissions)

            "priority":{
                        "coding":[{
                            "code":"EW EMER."}]},  //F:admission_type(admissions)


            "period":{
                    "start":"2147-12-30T08:40:00-05:00",    //C:admittime(admissions)
                    "end":"2148-01-11T17:55:00-05:00"},      //D:dischtime(admissions)

            "hospitalization":{
                    "admitSource":{
                            "coding":[
                                    {
                                    "code":"EMERGENCY ROOM"}]},   //G:admission_location(admissions)
                                    },

            "location":[
                // n time locations in the encounter based on the number of same id row

                    {"location":{
                        "reference":"Location/Emergency Department"},
                        "period":{
                            "start":"2147-12-30T06:45:00-05:00",   //M:edregtime(admissions)    F:intime(transfers)
                            "end":"2147-12-30T09:33:00-05:00"}},   //N:edouttime(admissions)    G:outtime(transfers)
                            
                    {"location":{
                                "reference":"Location/Trauma SICU (TSICU)"},
                                "period":{
                                "start":"2147-12-30T09:33:00-05:00",    //F:intime(transfers)
                                "end":"2148-01-02T23:24:32-05:00"}},              //G:outtime(transfers)
                    {"location":{
                                "reference":"Location/Trauma SICU (TSICU)"},   
                                "period":{"start":"2148-01-02T23:24:32-05:00",    //F:intime(transfers)
                                "end":"2148-01-08T18:14:21-05:00"}},              //G:outtime(transfers)

                    {"location":{
                                "reference":"Location/Med/Surg/Trauma"},
                                "period":{
                                    "start":"2148-01-08T18:14:21-05:00",          //F:intime(transfers)
                                    "end":"2148-01-11T17:55:24-05:00"}}]          //G:outtime(transfers)

}