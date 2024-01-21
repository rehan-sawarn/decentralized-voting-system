contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'
contract_abi =[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ballotName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_candidateName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_partyLogo",
				"type": "string"
			}
		],
		"name": "addParty",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ballotName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_ballotImage",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_startTime",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_endTime",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "_entryRestriction",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "_candidateName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_partyLogo",
				"type": "string"
			}
		],
		"name": "createBallot",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ballotName",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_partyIndex",
				"type": "uint256"
			}
		],
		"name": "voteForParty",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "ballotNames",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "ballots",
		"outputs": [
			{
				"internalType": "string",
				"name": "ballotImage",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "startTime",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "endTime",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "entryRestriction",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllBallotNames",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ballotName",
				"type": "string"
			}
		],
		"name": "getAllParties",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "candidateName",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "noOfVotes",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "partyLogo",
						"type": "string"
					}
				],
				"internalType": "struct Ballot.Party[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ballotName",
				"type": "string"
			}
		],
		"name": "getResults",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "candidateName",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "noOfVotes",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "partyLogo",
						"type": "string"
					}
				],
				"internalType": "struct Ballot.Party[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]